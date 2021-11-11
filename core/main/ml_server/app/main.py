from datetime import datetime
import logging
from logging.config import dictConfig

from .utils.ml_runner import run
from .utils.data_getter import get_data
from .utils.influxdb import connect_db, disconnect_db, get_database
from .utils.log_config import LogConfig
from fastapi_utils.tasks import repeat_every
from datetime import datetime
from fastapi import FastAPI
from .config import org, bucket


# logging.basicConfig(level=logging.DEBUG)
dictConfig(LogConfig().dict())

app = FastAPI(debug=True)
logger = logging.getLogger("API")

app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", disconnect_db)

running = False


@app.on_event('startup')
@repeat_every(seconds=10)
def run_ml_model():
    global running
    if running:
        return
    running = True
    logger.debug("RUNNING ML")
    data = get_data()
    logger.debug(f"DATA LEN: {data}")
    value = run(data)
    logger.debug(f"ML MODEL RESULT {value}")
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
    db.write(
        bucket=bucket,
        org=org,
        record=f"prediction device={value} {int(datetime.utcnow().timestamp() * 1e6)}000",
    )
    running = False
