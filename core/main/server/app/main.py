from typing import Optional
from datetime import datetime

from fastapi import FastAPI, Depends, Body, BackgroundTasks
from .utils.influxdb import connect_db, disconnect_db, get_database
from .utils.data_pusher import push_data
from influxdb_client.client.write_api import WriteApi
from pydantic import BaseModel

app = FastAPI()

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)

org = "gurkiratsingh2001@gmail.com"
bucket = "esw"


@app.post("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None, db: WriteApi = Depends(get_database)):

    data = f"mem,host=host1 exact_current={item_id}"
    print(data)
    db.write(bucket, org, data)
    return {"item_id": item_id, "q": q}


@app.post('/om2m-callback')
async def om2m_callback(background_tasks: BackgroundTasks, body=Body(...), db=Depends(get_database)):
    print("Body got")
    points = body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']
    points = points.split(',')
    points = [float(point) for point in points]
    print(len(points))
    delay = points[0]
    current = points[1:]
    timestamp = datetime.utcnow()
    print("Here")
    data_to_push = push_data(delay, current, timestamp)
    print(f"Pushing {data_to_push}")
    db.write(bucket=bucket, org=org, record=data_to_push)
    print("Pushed")
    # background_tasks.add_task(push_data, delay, current, timestamp)

    return "Success"
