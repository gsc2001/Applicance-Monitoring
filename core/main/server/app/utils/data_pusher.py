from fastapi import Depends
from datetime import datetime, timedelta
from .influxdb import get_database
from influxdb_client import WriteApi
# from config import org, bucket

org = "gurkiratsingh2001@gmail.com"
bucket = "esw"


def push_data(delay, points, timestamp: datetime):
    data_to_push = []
    current_time = timestamp
    dt = timedelta(milliseconds=delay)
    for point in points[::-1]:
        data_to_push.append(f"prediction current={point} {int(current_time.timestamp() * 1e6)}000")
        current_time = current_time - dt
    data_to_push = data_to_push[::-1]
    return data_to_push
    # db.write(bucket=bucket, org=org, record=data_to_push)
    # db = await get_database()
    # print(f"Writing Data! {len(data_to_push)}")
    # db.write(bucket=bucket, org=org, record=data_to_push)
