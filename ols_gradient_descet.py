# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 16:37:44 2019

@author: tothp
"""

#%%

import matplotlib.pyplot as pl
import numpy as np

n_samples = 100

x = np.linspace(0, 1, n_samples)
y = 3.4 * x + 2.1

y += np.random.randn(*y.shape)

pl.plot(x, y, 'r.')

a = 0
b = 10

n_epochs = 300
learning_rate = 0.001

for i in range(n_epochs):
    
    pl.cla()
    pl.plot(x, y, '.')
    pl.plot(x, a * x + b, "r")
    pl.xlim([0, 1])
    pl.ylim([1.5, 6])
    pl.pause(0.01)
    
    d_l_d_a = np.sum( 2 * ( a * x + b - y ) * x )
    d_l_d_b = np.sum( 2 * ( a * x + b - y ) * 1.0 )
    
    a -= learning_rate * d_l_d_a
    b -= learning_rate * d_l_d_b    
    