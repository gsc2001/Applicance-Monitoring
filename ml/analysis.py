import sys
import numpy as np
import pandas as pd
import pickle
import json
import matplotlib.pyplot as plt
import statistics

from sklearn.model_selection import train_test_split

from sktime.classification.dictionary_based import IndividualBOSS, ContractableBOSS, BOSSEnsemble
from sktime.classification.hybrid import HIVECOTEV1
from sktime.classification.kernel_based import ROCKETClassifier
from sktime.classification.shapelet_based import ShapeletTransformClassifier
from sktime.contrib.vector_classifiers._rotation_forest import RotationForest
from sktime.classification.interval_based import RandomIntervalSpectralForest, TimeSeriesForestClassifier
from sktime.classification.distance_based import KNeighborsTimeSeriesClassifier

from sktime.datasets import load_acsf1  # univariate dataset

SERIES_LEN = [300, 400, 500, 600, 1000, 1500]


# get X, y
def load_data(data, i):
    global SERIES_LEN
    appliance_labels = []
    current_time_series = []

    for key in data:
        series = data[key]['data']
        labels = key.split()
        label = labels[1]
        left = len(series)
        while left >= SERIES_LEN[i]:
            appliance_labels.append(label)
            current_time_series.append([pd.Series(series[len(series)-left : len(series)-left+SERIES_LEN[i]])])
            left = left - SERIES_LEN[i]

    df_current = pd.DataFrame(current_time_series)
    return df_current, np.array(appliance_labels)

json_data = []
with open('mod_data.json') as f:
  data = json.load(f)


models = []
models.append(('Rocket', ROCKETClassifier(num_kernels=500)))
models.append(('IndividualBOSS', IndividualBOSS()))
# models.append(('ContractableBOSS', ContractableBOSS(n_parameter_samples=25, max_ensemble_size=5)))
# models.append(('HIVECOTEV1', HIVECOTEV1(stc_params={"estimator": RotationForest(n_estimators=3), "n_shapelet_samples": 500, "max_shapelets": 20, "batch_size": 100}, 
                                                    # tsf_params={"n_estimators": 10}, rise_params={"n_estimators": 10}, cboss_params={"n_parameter_samples": 25, "max_ensemble_size": 5})))
models.append(('RISE', RandomIntervalSpectralForest(n_estimators=10)))
models.append(('TSForest', TimeSeriesForestClassifier()))
# models.append(('Shapelet', ShapeletTransformClassifier(estimator=RotationForest(n_estimators=3), n_shapelet_samples=500, max_shapelets=20, batch_size=100)))

# computationally heavy classifiers

# models.append(('BOSSEnsemble', BOSSEnsemble(max_ensemble_size=5)))
# models.append(('KNTs', KNeighborsTimeSeriesClassifier()))


mean_scores = []
model_scores = []
for i in range(len(models)):
    model_scores.append([])

for i in range(len(SERIES_LEN)):

    # load training and test data
    X, y = load_data(data, i)

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.67)

    # evaluate each model
    scores = []
    names = []

    print(str(SERIES_LEN[i]) + ' length series:')

    model_num = 0
    for name, model in models:
        model.fit(X_train, y_train)
        model_score = model.score(X_test, y_test)
        scores.append(model_score)
        model_scores[model_num].append(model_score)
        names.append(name)
        print("{:s}: {:.3f}".format(name, model_score))
        model_num = model_num + 1
    print()
    
    mean_scores.append(statistics.mean(scores))


model_num = 0
for name, model in models:
    plt.plot(SERIES_LEN, model_scores[model_num], label = str(name))
    model_num = model_num + 1

plt.plot(SERIES_LEN, mean_scores, label = "Mean Score")

plt.legend()

plt.savefig('graph_series_len.png')
