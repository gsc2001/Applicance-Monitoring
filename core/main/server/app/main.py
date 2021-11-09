from typing import Optional

from fastapi import FastAPI, Depends
from .utils.influxdb import connect_db, disconnect_db, get_database
from influxdb_client.client.write_api import WriteApi

app = FastAPI()

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)

org = "gurkiratsingh2001@gmail.com"
bucket = "gurkiratsingh2001's Bucket"


@app.post("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None, db: WriteApi = Depends(get_database)):
    data = f"mem,host=host1 used_percent={item_id}"
    db.write(bucket, org, data)
    return {"item_id": item_id, "q": q}
