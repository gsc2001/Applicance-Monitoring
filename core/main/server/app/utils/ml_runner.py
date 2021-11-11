from .ml_model import get_prediction
model = None


# def load_model():
#     pass


def run(data):
    value = get_prediction(data)
    return value
