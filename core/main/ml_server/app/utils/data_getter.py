from .influxdb import get_client
from ..config import bucket
import logging

logger = logging.getLogger("API")


def get_data():
    logger.debug("Getting data")
    query = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r._field == "current") |> sort(columns: ["_time"])'
    logger.debug("Getting data 2")
    client = get_client()
    logger.debug("Getting data 3")
    tables = client.query_api().query(query)
    logger.debug(f"Getting data {tables}")
    if len(tables) > 0:
        table = tables[0]
        logger.debug("")
        data = [rec.get_value() for rec in table.records]
    else:
        data = []
    return data
