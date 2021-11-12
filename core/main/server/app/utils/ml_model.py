import numpy as np
import pandas as pd
import pickle
#######################################################
from collections import Counter
########################################
FILE_NAME = "/code/app/utils/300_0.9_models.pckl"
model_key = {
    "Rocket_Classifier": "Rocket",
    "Individual_Boss": "IndividualBOSS",
    'RISE': "RISE",
    'TSForest': 'TSForest',
    'Shapelet': 'Shapelet'
}
models = dict()

with open(FILE_NAME, "rb") as f:
    models_dict = pickle.load(f)

###############################################


def ret_splitted_array(arr, each_sz=300):
    data = []
    tot_len = len(arr)
    num_parts = tot_len // each_sz
    actual_sz = num_parts * each_sz
    arr = arr[:actual_sz]
    if len(arr) == 0:
        return []
    ans = np.array_split(arr, num_parts)
    ans = [list(x) for x in ans]
    # print(type(ans))
    return ans


def get_correct_format(arr):
    ret_arr = []
    for curr_arr in arr:
        ret_arr.append([pd.Series(curr_arr)])
    return pd.DataFrame(ret_arr)


def get_prediction(input_arr, model_key="TSForest"):
    print("Number of data points obtained is ", len(input_arr))
    input_arr = ret_splitted_array(input_arr)
    print("Number of data points obtained after truncation is ", len(input_arr))
    if model_key not in models_dict:
        print("No such model exists")
        return None
    input_arr = get_correct_format(input_arr)

    # key exists
    prediction_labels = models_dict[model_key].predict(input_arr)
    # f_dict = Counter(prediction_labels)
    # print(f_dict)
    # max_f = -1
    # best_key = None
    # for curr_pred, pred_freq in f_dict.items():
    #     if pred_freq >= max_f:
    #         max_f = pred_freq
    #         best_key = curr_pred

    return prediction_labels
    # print("##########################")
    # return prediction_labels


# label_ans = get_prediction(arr)
