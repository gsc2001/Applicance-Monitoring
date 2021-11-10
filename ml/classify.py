import sys
import numpy as np
import pandas as pd
import pickle
import json

from sklearn.model_selection import train_test_split

from sktime.classification.dictionary_based import IndividualBOSS, ContractableBOSS, BOSSEnsemble
from sktime.classification.hybrid import HIVECOTEV1
from sktime.classification.kernel_based import ROCKETClassifier
from sktime.classification.shapelet_based import ShapeletTransformClassifier
from sktime.contrib.vector_classifiers._rotation_forest import RotationForest
from sktime.classification.interval_based import RandomIntervalSpectralForest, TimeSeriesForestClassifier
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier

from sktime.datasets import load_acsf1  # univariate dataset

SERIES_LEN = int(sys.argv[1])

# get X, y
def load_data(data):
    global SERIES_LEN
    appliance_labels = []
    current_time_series = []

    for key in data:
        series = data[key]['data']
        labels = key.split()
        label = labels[1]
        left = len(series)
        while left >= SERIES_LEN:
            appliance_labels.append(label)
            current_time_series.append([pd.Series(series[len(series)-left : len(series)-left+SERIES_LEN])])
            left = left - SERIES_LEN

    df_current = pd.DataFrame(current_time_series)
    return df_current, np.array(appliance_labels)

json_data = []
with open('mod_data.json') as f:
  data = json.load(f)


# load training and test data
X, y = load_data(data)
# for i in range(len(X[0])):
#     print(y[i])
#     print(len(X[0][i]))

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.67)

# # loading acsf1 data
# X_train, y_train = load_acsf1(split="train", return_X_y=True)
# X_test, y_test = load_acsf1(split="test", return_X_y=True)
# # print(type(y_test))
# # print(type(X_test['dim_0']))

models = []
models.append(('Rocket', ROCKETClassifier(num_kernels=500)))
models.append(('IndividualBOSS', IndividualBOSS()))
# models.append(('ContractableBOSS', ContractableBOSS(n_parameter_samples=25, max_ensemble_size=5)))
# models.append(('HIVECOTEV1', HIVECOTEV1(stc_params={"estimator": RotationForest(n_estimators=3), "n_shapelet_samples": 500, "max_shapelets": 20, "batch_size": 100}, 
                                                    # tsf_params={"n_estimators": 10}, rise_params={"n_estimators": 10}, cboss_params={"n_parameter_samples": 25, "max_ensemble_size": 5})))
models.append(('RISE', RandomIntervalSpectralForest(n_estimators=10)))
models.append(('TSForest', TimeSeriesForestClassifier()))
models.append(('Shapelet', ShapeletTransformClassifier(estimator=RotationForest(n_estimators=3), n_shapelet_samples=500, max_shapelets=20, batch_size=100)))


# computationally heavy classifiers

# models.append(('BOSSEnsemble', BOSSEnsemble(max_ensemble_size=5)))
# models.append(('KNTs', KNeighborsTimeSeriesClassifier()))

# evaluate each model
scores = []
names = []

for name, model in models:
    model.fit(X_train, y_train)
    model_score = model.score(X_test, y_test)
    scores.append(model_score)
    names.append(name)
    print("{:s}: {:.3f}".format(name, model_score))

with open(str(SERIES_LEN) + "_models.pckl", "wb") as f:
    for model in models:
        pickle.dump(model, f)


# Results on acsf1:
# Rocket: 0.830
# IndividualBOSS: 0.810
# ContractableBOSS: 0.720
# HIVECOTEV1: 0.800
# RISE: 0.790
# TSForest: 0.670
# Shapelet: 0.760