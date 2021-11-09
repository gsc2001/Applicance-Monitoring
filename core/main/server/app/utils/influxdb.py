from datetime import datetime

import os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, WriteApi
# import config

DATABASE_URL = os.getenv('DATABASE_URL', None)
DATABASE_TOKEN = os.getenv('DATABASE_TOKEN', None)


class Database:
    client: InfluxDBClient = None
    write_api: WriteApi = None


db = Database()

org = "gurkiratsingh2001@gmail.com"


def connect_db():
    db.client = InfluxDBClient(url=DATABASE_URL, token=DATABASE_TOKEN, org=org)
    db.write_api = db.client.write_api(write_options=SYNCHRONOUS)


def disconnect_db():
    db.client.close()


def get_database() -> InfluxDBClient:
    return db.write_api
