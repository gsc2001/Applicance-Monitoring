import math
from fastapi import Depends
from datetime import datetime, timedelta
from .influxdb import get_database
from influxdb_client import WriteApi

# from config import org, bucket

org = "gurkiratsingh2001@gmail.com"
bucket = "esw"


def preprocess_data(delay, points, timestamp: datetime):
    data_to_push = []
    current_time = timestamp
    dt = timedelta(milliseconds=delay)
    for point in points[::-1]:
        data_to_push.append(
            f"prediction current={point} {int(current_time.timestamp() * 1e6)}000"
        )
        current_time = current_time - dt
    data_to_push = data_to_push[::-1]
    return data_to_push


def preprocess_rms_data(delay, points, timestamp: datetime):
    rms = 0

    for point in points:
        rms += point ** 2

    rms /= len(points)
    rms = math.sqrt(rms)

    return [f"prediction current_rms={rms} {int(timestamp.timestamp() * 1e6)}000"]


def preprocess_step_data(delay, points, timestamp):
    data_to_push = []
    current_time = timestamp
    dt = timedelta(milliseconds=delay)
    for point in points[::-1]:
        data_to_push.append(
            f"prediction current_step={point} {int(current_time.timestamp() * 1e6)}000"
        )
        current_time = current_time - dt
    data_to_push = data_to_push[::-1]
    return data_to_push[::10]


def get_preceprocess_data(delay, points, timestamp):
    data = []
    data.extend(preprocess_data(delay, points, timestamp))
    data.extend(preprocess_rms_data(delay, points, timestamp))
    data.extend(preprocess_step_data(delay, points, timestamp))
    return data
