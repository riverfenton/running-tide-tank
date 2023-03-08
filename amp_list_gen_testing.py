# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 15:46:03 2023

@author: User
"""

import numpy as np
from TFs import TFs
from fileOperations import fileOperations
from frequency_conversions import freq_conv
import create_nLf_LUT as create_csv
import pandas as pd


def read_nLf():
    #Creates CSV of allowed frequencies
    create_csv
    mode_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[0])
    mode_list=mode_list.values.tolist()
    
    length_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[1])
    length_list=length_list.values.tolist()
    
    freq_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[2])
    freq_list=round(freq_list, 2)
    freq_list=freq_list.values.tolist()
    
    amp_list = pd.read_csv('nLfA_sort.csv', header=None, usecols=[3])
    amp_list=amp_list.values.tolist()
    
    return freq_list, mode_list, length_list, amp_list

[freq_list, mode_list, length_list, amp_list]=read_nLf()

def gen_amp_sel_list(amp_list, selection_index):
    whole_TF=amp_list[selection_index]
    [_, _, _, _, _, _, _, crank_shaft, num_stroke]=fileOperations.load_params()
    allowable_stroke=np.linspace(0,crank_shaft,num_stroke)
    allowable_amp=allowable_stroke*whole_TF
    
    return allowable_stroke, allowable_amp

selection_index=4 #for example. actually chosen by users frequency selection
whole_TF=amp_list[selection_index]

if (int(mode_list[selection_index][0])==2):
    [allowable_stroke, allowable_amp]=gen_amp_sel_list(amp_list, selection_index)
    #populate list etc
    print('pop up amplitude selection screen')
else:
    print('pop up warning screen')
    
def gen_amp_sel_list(amp_list, selection_index):
    whole_TF=amp_list[selection_index]
    [_, _, _, _, _, _, _, crank_shaft, num_stroke]=fileOperations.load_params()
    allowable_stroke=np.linspace(0,crank_shaft,num_stroke)
    allowable_amp=allowable_stroke*whole_TF
    
    return allowable_stroke, allowable_amp


    
    
        