# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 15:24:28 2023

@author: User
"""

#the purpose of this script is to generate the look up tables used in the the
#frequency and amplitude dropdown menus. It uses filOperations.load_params() to
#pull the necessary parameters to perform the calculation, then uses TFs.TF_res
#and TFs.TF_tank to perform the calculations. It then saves a CSV file. Each 
#row of the csv contains (in order) the normal mode number, the tank length 
#(meters), the frequency (rpm), and the ratio of stroke length to wave height
#at that frequency. The csv is sorted in ascending order according to frequency


import numpy as np
from TFs import TFs
from fileOperations import fileOperations
from frequency_conversions import freq_conv

[h, L_max, L_min, num_L, n_min, n_max, paddle, crank_shaft, num_s]=fileOperations.load_params()

L=np.linspace(L_min,L_max,num_L) #set of allowable lengths
n=np.asarray(list(range(n_min,n_max+1))) #set of allowable normal modes

nLfA=np.empty([len(L)*len(n),4]) #list of 4-tuples. Each tuple
                                #contains a different combo of [n,L,f,A]
                                
s_ratio=paddle/h; #similar triangles; stroke at water height compared to stroke
                    #at height of motor

for i in range(len(L)): #calculating the values for f in the nLf matrix
    w, H_res = TFs.TF_res(n,L[i],h)
    H_tank= TFs.TF_tank(w,h)
    lower_ind=i*len(n)
    upper_ind=(i+1)*len(n)
    nLfA[lower_ind:upper_ind,0]=n
    nLfA[lower_ind:upper_ind,1]=L[i]
    nLfA[lower_ind:upper_ind,2]=freq_conv.w_2_rpm(w)
    nLfA[lower_ind:upper_ind,3]=np.multiply(H_res,H_tank)*2/s_ratio
    #this last line takes into accont wave superposition (*H_tank), the fact
    #that the crank shaft radius creates a stroke equal to its diameter (*2)
    #and the stroke differnece at water surface compared to motor height(/s_ratio)
    
indcs=np.argsort(nLfA[:,2]) #find the indices that sort nLf according to freq

nLfA_sorted=np.empty_like(nLfA)
nLfA_sorted[:,:]=nLfA[indcs,:]

np.savetxt('nLfA_sort.csv',nLfA_sorted,delimiter=',')