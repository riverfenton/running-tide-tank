# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 14:00:02 2023

@author: User
"""

import numpy as np

class TFs:
    
    def TF_tank(w, h):
        
        #transfer function for waves created by rotating paddle
        #paddle stroke length --> height of outgoing wave
        
        #ARGUMENTS
        # w: angular frequency - numpy array
        # h: water height - scalar
        
        g=9.81 #gravity (m/s^2)
        k=np.multiply(w,w)/g #see justification below
        
        #calculation goes
        #for sinusoid, phase velocity c= w/k. in deepwater,c=sqrt(g/k)
        #so w=k*sqrt(g/k) ---> k=w^2/g
        
        num = np.multiply( (4*np.sinh(k*h)) , (np.multiply(k*h , np.sinh(k*h))-np.cosh(k*h)+1) )
        den = np.multiply(k*h,(np.sinh(2*k*h)+2*k*h));
        
        amp=np.divide(num,den)
        return amp #transfer function amplitude (real number)

    def TF_res(n, L, h):
        
        #transfer function for the effects of wave interference
        #height of outgoing wave --> height of (outgoing + reflected) waves
        
        #ARGUMENTS
        # n: "mode number" - numpy array
        # L: tank length - scalar
        # h: water height - scalar
        
        
        #n should be a vector representing "mode number"
        #n=1 first normal mode number, n=2 second normal mode, etc.
        #fractional n represents some amount of phase cancellation
        
        #we use n to calculate w instead of w to calculate n because
        #there is a closed form expression for w(n) but not for n(w)
            
        g=9.81 #gravity (m/s^2)

        w=np.sqrt(np.multiply( (n*np.pi*g/L) ,np.tanh(n*np.pi*h/L) ))#angular frequency
        H_res=1+np.cos(2*np.pi*n) #allows for interpreting sinusoidally between peaks
      
        
        
        return w, H_res
    