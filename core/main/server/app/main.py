from pydantic import BaseModel
from influxdb_client.client.write_api import WriteApi
from .utils.ml_model import run
from .utils.data_getter import get_data
from .utils.data_pusher import push_data
from .utils.influxdb import connect_db, disconnect_db, get_database
from fastapi_utils.tasks import repeat_every
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Depends, Body, BackgroundTasks
import logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()
logger = logging.getLogger('API')

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)

org = "gurkiratsingh2001@gmail.com"
bucket = "esw"


@app.post("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None, db: WriteApi = Depends(get_database)):

    data = f"mem,host=host1 exact_current={item_id}"

    db.write(bucket, org, data)
    return {"item_id": item_id, "q": q}


@app.post('/om2m-callback')
async def om2m_callback(body=Body(...), db=Depends(get_database)):
    print("Body got")
    points = body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
    points = points.split(',')
    points = [float(point) for point in points]
    logger.info(f"DATA {len(points)}")
    delay = points[0]
    current = points[1:]
    timestamp = datetime.utcnow()
    logging.info("Here")
    data_to_push = push_data(delay, current, timestamp)
    logging.info(f"Pushing {data_to_push}")
    db.write(bucket=bucket, org=org, record=data_to_push)
    logging.info("Pushed")
    # background_tasks.add_task(push_data, delay, current, timestamp)

    return "Success"


@app.on_event('startup')
@repeat_every(seconds=5)
def run_ml_model():
    logging.info("Running ML")
    data = get_data()
    value = run(data)
    logger.info(f"ML RESULT {value}")
    value = 2019
    db = get_database()
    db.write(bucket=bucket, org=org, record=f"prediction device={value}")
