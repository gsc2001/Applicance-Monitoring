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

#######################################################

FILE_NAME="300_0.8_models.pckl"
model_key={
    "Rocket_Classifier":"Rocket",
    "Individual_Boss":"IndividualBOSS",
    'RISE':"RISE",
    'TSForest':'TSForest',
    'Shapelet':'Shapelet'
}
models=dict()

with open(FILE_NAME, "rb") as f:
    models_dict=pickle.load(f)
print(models_dict)
print(models_dict.keys())