import os

current_label_freq_dict = None
data_yet = None
tot_times_data_received = None
pending_labels = None


def vars_init():
    global current_label_freq_dict, data_yet, tot_times_data_received, pending_labels

    pending_labels = []
    current_label_freq_dict = {}
    data_yet = []
    tot_times_data_received = 0
    # tot_iterations_currently=0
