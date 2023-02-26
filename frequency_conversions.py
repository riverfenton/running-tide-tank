# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 10:42:20 2023

@author: User
"""

import numpy as np

class freq_conv:
    
    def f_2_w(f):
        w=2*np.pi*f
        return w
    
    def f_2_rpm(f):
        rpm=60*f
        return rpm
    
    def w_2_rpm(w):
        rpm=freq_conv.f_2_rpm(freq_conv.w_2_f(w))
        return rpm
    
    def w_2_f(w):
        f=w/(2*np.pi)
        return f
    
    def rpm_2_f(rpm):
        f=rpm/60
        return f
    
    def rpm_2_w(rpm):
        w=freq_conv.rpm_2_f(freq_conv.f_2_w(rpm))
        return w
        