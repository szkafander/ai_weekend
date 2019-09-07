# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 15:13:18 2019

@author: tothp
"""
#%%
import numpy as np
import matplotlib.pyplot as pl

n_samples = 100

x = np.linspace(0, 1, n_samples)
y = 3.4 * x + 2.1

y += np.random.randn(*y.shape)

pl.plot(x, y, 'r.')

# y_hat = f(x) = beta * x
x = np.expand_dims(x, -1)
y = np.expand_dims(y, -1)

x = np.hstack((x, np.ones(x.shape)))

beta_hat = np.matmul(
        np.linalg.inv(
                np.matmul(x.T, x)
            ), 
        np.matmul(x.T, y)
    )
        
pl.plot(x, np.matmul(x, beta_hat), "b")