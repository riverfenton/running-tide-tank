# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 16:51:22 2023

@author: User
"""

class fileOperations:
    
    def load_params():
        with open('params.txt') as f:
            lines=f.readlines()
    
        for line in lines:
            if line[0:12] == "Water Height":
                h=float(line[14:18])
            elif line[0:16] == "Full Tank Length":
                L_max=float(line[18:22])
            elif line[0:12] == "Track Length":
                L_min=L_max-float(line[14:18])
            elif line[0:25] == "Number of Length Settings":
                num_L=int(line[27:29])
            elif line[0:19] == "Minimum Normal Mode":
                n_min=int(line[21:22])
            elif line[0:19] == "Maximum Normal Mode":
                n_max=int(line[21:22])
                
        return h, L_max, L_min, num_L, n_min, n_max