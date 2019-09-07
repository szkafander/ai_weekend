# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 16:58:23 2019

@author: tothp
"""
#%%
import matplotlib.pyplot as pl
import numpy as np

def f(x):
    return x ** 2

def df_dx(x):
    return 2 * x

x = 5.0

x_ = np.linspace(-6, 6, 50)
y_ = f(x_)

n_epochs = 100
learning_rate = 0.025

for i in range(n_epochs):
    
    pl.cla()
    pl.plot(x_, y_, "b")
    
    f_x = f(x)
    
    pl.plot(x, f_x, "or")
    
    df_dx_x = df_dx(x)
    
    x -= learning_rate * df_dx_x
    
    pl.title("x at {}".format(x))
    
    pl.pause(0.01)
    
#%% with emulated "noise"
    
def f(x):
    return x ** 2 + np.sin(x * 4) * 1.5

def df_dx(x):
    return 2 * x + 1.5 * np.cos(x * 4) * 4

x_ = np.linspace(-6, 6, 200)
y_ = f(x_)

n_epochs = 100
learning_rate = 0.01

x = 5.0

for i in range(n_epochs):
    
    pl.cla()
    pl.plot(x_, y_, "b")
    
    f_x = f(x)
    
    pl.plot(x, f_x, "or")
    
    df_dx_x = df_dx(x)
    
    x -= learning_rate * df_dx_x
    
    pl.title("x at {}".format(x))
    
    pl.pause(0.01)
    
#%% momentum
    
n_epochs = 150
learning_rate = 0.01
beta = 0.93

x = 5.0

for i in range(n_epochs):
    
    pl.cla()
    pl.plot(x_, y_, "b")
    
    f_x = f(x)
    
    pl.plot(x, f_x, "or")
    
    df_dx_x = df_dx(x)
    
    if i == 0:
        dx = df_dx_x
    else:
        dx = beta * dx + (1 - beta) * df_dx_x
    
    x -= learning_rate * dx
    
    pl.title("x at {}".format(x))
    
    pl.pause(0.01)