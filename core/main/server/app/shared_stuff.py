import os

def vars_init():
    global current_label_freq_dict,data_yet,tot_times_data_received,pending_labels

    pending_labels=[]
    current_label_freq_dict={}
    data_yet=[]
    tot_times_data_received=0
    # tot_iterations_currently=0