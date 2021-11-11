from datetime import datetime
import logging
from logging.config import dictConfig

from .utils.data_pusher import get_preceprocess_data
from .utils.influxdb import connect_db, disconnect_db, get_database
from .utils.log_config import LogConfig
from datetime import datetime
from fastapi import FastAPI, Depends, Body
from .config import org, bucket


# logging.basicConfig(level=logging.DEBUG)
dictConfig(LogConfig().dict())

app = FastAPI(debug=True)
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
