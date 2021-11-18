from datetime import datetime
import logging
from logging.config import dictConfig
from . import shared_stuff as gv
from pydantic import BaseModel
from influxdb_client.client.write_api import WriteApi

from .utils.ml_runner import run
from .utils.data_getter import get_data
from .utils.data_pusher import get_preceprocess_data
from .utils.influxdb import connect_db, disconnect_db, get_database
from .utils.log_config import LogConfig
from .utils.decrypt import decrypt_string
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from fastapi import FastAPI, Depends, Body
from .config import org, bucket

from collections import deque


# logging.basicConfig(level=logging.DEBUG)
dictConfig(LogConfig().dict())

app = FastAPI(debug=True)
logger = logging.getLogger("API")

# init global variables
gv.vars_init()

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)


@app.get("/test")
async def test():
    logger.debug("TEST!")
    logger.info("TEST!")
    logger.warning("TEST!")
    return "Check"

# cnt=0
# counter=0
# data_arr=[]
@app.post("/om2m-callback")
async def om2m_callback(body=Body(...), db=Depends(get_database)):
   
    # incrementing the 
    gv.tot_times_data_received+=1
    logger.info("Total times data received all the times so far")
    logger.debug(str(gv.tot_times_data_received))
    

    # extracting data from OneM2m resource tree
    encrypted = body["m2m:sgn"]["m2m:nev"]["m2m:rep"]["m2m:cin"]["con"]
    # print(encrypted)
    points = decrypt_string(encrypted)
    # logger.debug(str(points));
    points = points.split(",")
    points = [float(point) for point in points]
    delay = points[0]

    # finding the new data received
    current = points[1:]
    timestamp = datetime.utcnow()

    # appending the newly receved data to my global array
    gv.data_yet.extend(current)

    
    data_to_push = get_preceprocess_data(delay, current, timestamp)
    db.write(bucket=bucket, org=org, record=data_to_push)

    # run ml_model every 3 seconds
    if gv.tot_times_data_received%3==0:
        run_ml_model()
        # empty data array
        gv.data_yet=[]
    # return "Successful Modified"

    return "Success"

MAX_QUEUE_SIZE=5
LABEL_DEQUE=deque()

def run_ml_model():
    # logger.debug("RUNNING ML")

    value_arr = run(gv.data_yet)
    for curr_label in value_arr:
        try:
            gv.current_label_freq_dict[curr_label]+=1
        except:
            gv.current_label_freq_dict[curr_label]=1
        LABEL_DEQUE.append(curr_label)
        if len(LABEL_DEQUE)>MAX_QUEUE_SIZE:
            label_to_exlude=LABEL_DEQUE.popleft()
            gv.current_label_freq_dict[label_to_exlude]-=1
    

    
    print(gv.current_label_freq_dict)

    # fetch most frequent label
    max_cnt=0
    best_label="No device"
    for curr_label, label_freq in gv.current_label_freq_dict.items():
        if label_freq>max_cnt:
            max_cnt=label_freq
            best_label=curr_label
    print("Currently want to predict ", best_label)

    # value="WM"
    value_encode = {
        "WM": 1,
        "HD": 2,
        "MW": 3,
        "IR": 4,
        "VC": 5,
        "MG": 6,
        "EK": 7,
        "GY": 8,
        "TV":9,
        "Oil Heater":10
    }
    value = value_encode.get(best_label, 0)

    db = get_database()
    db.write(
        bucket=bucket,
        org=org,
        record=f"prediction device={value} {int(datetime.utcnow().timestamp() * 1e6)}000",
    )
