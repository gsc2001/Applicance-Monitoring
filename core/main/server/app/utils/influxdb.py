from datetime import datetime

import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS, SYNCHRONOUS, WriteApi, WriteOptions
# import config

DATABASE_URL = os.getenv('DATABASE_URL', None)
DATABASE_TOKEN = os.getenv('DATABASE_TOKEN', None)


class Database:
    client: InfluxDBClient = None
    write_api: WriteApi = None


db = Database()

org = "gurkiratsingh2001@gmail.com"


async def connect_db():
    db.client = InfluxDBClient(url=DATABASE_URL, token=DATABASE_TOKEN, org=org,debug=True)
    db.write_api = db.client.write_api(write_options=WriteOptions())


async def disconnect_db():
    db.client.close()


async def get_database() -> InfluxDBClient:
    return db.write_api
