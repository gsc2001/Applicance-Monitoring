import pickle
import sys
import pandas as pd

# Rocket, IndividualBOSS, ContractableBOSS, HIVECOTEV1, RISE, TSForest, Shapelet

SERIES_LEN = int(sys.argv[1])

# get X
def load_data(series):
    global SERIES_LEN

    current_time_series = []
    left = len(series)
    while left >= SERIES_LEN:
        current_time_series.append([pd.Series(series[len(series)-left : len(series)-left+SERIES_LEN])])
        left = left - SERIES_LEN

    df_current = pd.DataFrame(current_time_series)
    return df_current

# load models
models = []
with open(str(SERIES_LEN) + "_models.pckl", "rb") as f:
    while True:
        try:
            models.append(pickle.load(f))
        except EOFError:
            break

# take input for testing
input = [0.0] * SERIES_LEN
X_test = load_data(input)

# model predictions
predictions = []

for name, model in models:
    pred_val = model.predict(X_test)
    predictions.append(pred_val[0])
    print("{:s}: {:s}".format(name, pred_val[0]))

print(predictions)