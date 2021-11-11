import logging
from .ml_model import get_prediction
model = None


# def load_model():
#     pass
logger = logging.getLogger("API")


def run(data):
    logger.debug("in runner")
    value = get_prediction(data)
    return value
