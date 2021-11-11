import os
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import WriteApi, WriteOptions
from ..config import org

DATABASE_URL = os.getenv('DATABASE_URL', None)
DATABASE_TOKEN = os.getenv('DATABASE_TOKEN', None)


class Database:
    client: InfluxDBClient = None
    write_api: WriteApi = None


db = Database()


async def connect_db():
    # logger.info("Connecting to DB")
    db.client = InfluxDBClient(url=DATABASE_URL, token=DATABASE_TOKEN, org=org)
    db.write_api = db.client.write_api(write_options=WriteOptions())


async def disconnect_db():
    # logger.info("DB connection stoped")
    db.client.close()


def get_database() -> WriteApi:
    return db.write_api


def get_client() -> InfluxDBClient:
    return db.client
