import logging
from .influxdb import get_client


def get_data():
    query = 'from(bucket: "esw") |> range(start: -1h) |> filter(fn: (r) => r._field == "current") |> sort(columns: ["_time"])'
    client = get_client()
    tables = client.query_api().query(query)
    table = tables[0]
    data = [rec.get_value() for rec in table.records]
    logging.info(f"DATA {len(data)}")
    return data
