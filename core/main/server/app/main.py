import logging
from .utils.ml_runner import run
from .utils.data_getter import get_data
from .utils.data_pusher import get_preceprocess_data
from .utils.influxdb import connect_db, disconnect_db, get_database
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from fastapi import FastAPI, Depends, Body
from config import org, bucket


# logging.basicConfig(level=logging.DEBUG)

app = FastAPI()
logger = logging.getLogger("API")

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)


@app.post("/om2m-callback")
async def om2m_callback(body=Body(...), db=Depends(get_database)):
    points = body["m2m:sgn"]["m2m:nev"]["m2m:rep"]["m2m:cin"]["con"]
    points = points.split(",")
    points = [float(point) for point in points]
    delay = points[0]
    current = points[1:]
    timestamp = datetime.utcnow()
    data_to_push = get_preceprocess_data(delay, current, timestamp)
    db.write(bucket=bucket, org=org, record=data_to_push)

    return "Success"


@app.on_event("startup")
@repeat_every(seconds=60)
def run_ml_model():
    data = get_data()
    value = run(data)
    value_encode = {
        "WM": 1,
        "HD": 2,
        "MW": 3,
        "IR": 4,
        "VC": 5,
        "MG": 6,
        "EK": 7,
        "GY": 8,
    }
    value = value_encode.get(value, 0)
    db = get_database()
    db.write(bucket=bucket, org=org, record=f"prediction device={value}")
