# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 16:51:22 2023

@author: User
"""

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
        