# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:09:30 2019

@author: tothp
"""
#%%
import matplotlib.pyplot as pl
import numpy as np

def f(x):
    return x ** 2

x = 5.0

x_ = np.linspace(-6, 6, 200)
y_ = f(x_)

n_epochs = 100
n_trials = 10
shrinking_factor = 0.9
range_ = [-6, 6]

for i in range(n_epochs):
    
    full_range = range_[1] - range_[0]
    center_of_range = np.mean(range_)
    
    pl.cla()
    pl.plot(x_, y_, "b")
    pl.xlim([-6, 6])
    pl.ylim([-5, 36])
    
    trials = (np.random.rand(n_trials) * full_range) + range_[0]
    f_x = f(trials)
    
    pl.plot(trials, f_x, "ro")
    
    min_x = trials[np.argmin(f_x)]
    
    range_ = [
            min_x - full_range / 2 * shrinking_factor,
            min_x + full_range / 2 * shrinking_factor
        ]
    
    pl.title("x at {}".format(min_x))
    pl.pause(0.01)

#%%
    
def f(x):
    return x ** 2 + np.sin(x * 4) * 1.5

def df_dx(x):
    return 2 * x + 1.5 * np.cos(x * 4) * 4

x_ = np.linspace(-6, 6, 200)
y_ = f(x_)