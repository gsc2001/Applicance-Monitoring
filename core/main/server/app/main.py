from typing import Optional

from fastapi import FastAPI, Depends, Body
from .utils.influxdb import connect_db, disconnect_db, get_database
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


@app.post('/test')
async def om2m_callback(body=Body(...)):

    return "Success"
