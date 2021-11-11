from .influxdb import get_client
from ..config import bucket


def get_data():
    query = f'from(bucket: {bucket}) |> range(start: -1h) |> filter(fn: (r) => r._field == "current") |> sort(columns: ["_time"])'
    client = get_client()
    tables = client.query_api().query(query)
    table = tables[0]
    data = [rec.get_value() for rec in table.records]
    return data
