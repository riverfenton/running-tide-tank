# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 16:51:22 2023

@author: User
"""

#load_params reads from a .txt file and saves the relevant parameter info as
#variables. This function assumes a very specific form for the .txt file. The
#lines of the file are as follows:
    #line 0: depth of water in tank in meters (saved as h)
    #line 1: maximum length of the tank in meters. Should be measured from the
        #wall behind the wavemaker paddle to the furthes allowable position of
        #the back wall (saved as L_max)
    #line 2: track length in meters. range of backwall motion used to calculate
        #the variable L_min
    #line 3: number of allowable length settings (integer). not a physical
        #parameter, but a number used to determine how much resolution the
        #options from the frequency drop down menu will have (saved as num_L)
    #line 4: minimum allowable normal mode (integer). The Dartmouth engineering
        #team had trouble generating waves in the first mode, so we suggest
        #this number to 2 (saved as n_min)
    #line 5: maximum allowable normal mode (integer). The Dartmouth engineering
        #team found that anywhere above 80 rpm the waves become excessively
        #chaotic, so restricing the max normal mode to 4 removes this
        #possibility for the most part (saved as n_max)
    #line 6: height of the wave generating paddle in meters (saved as paddle)
    #line 7: maximum extension of the crank shaft mechanism measured in inches
        #(saved as crank_shaft)
    #line 8: number of allowable stroke settings (integer). similar to num_L,
        #this is used to control the resolution of the dropdown menu, though in
        #this case for amplitude (saved as num_s)
        

class fileOperations:
    
    def load_params():
        with open('params_test.txt') as f:
            lines=f.readlines()
    
        h = float(lines[0]) #m
        L_max = float(lines[1]) #m
        L_min = L_max - float(lines[2]) #m
        num_L = int(lines[3]) #m
        n_min = int(lines[4])
        n_max = int(lines[5])
        paddle = float(lines[6]) #m
        crank_shaft = float(lines[7]) #in
        num_s = int(lines[8])
        
        return h, L_max, L_min, num_L, n_min, n_max, paddle, crank_shaft, num_s
    
        # for line in lines:
        #     if line[0:12] == "Water Height":
        #         h=float(line[14:18])
        #     elif line[0:16] == "Full Tank Length":
        #         L_max=float(line[18:22])
        #     elif line[0:12] == "Track Length":
        #         L_min=L_max-float(line[14:18])
        #     elif line[0:25] == "Number of Length Settings":
        #         num_L=int(line[27:29])
        #     elif line[0:19] == "Minimum Normal Mode":
        #         n_min=int(line[21:22])
        #     elif line[0:19] == "Maximum Normal Mode":
        #         n_max=int(line[21:22])
                
        # return h, L_max, L_min, num_L, n_min, n_max
        