# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 21:58:02 2019

@author: tothp
"""
#%%
import numpy as np
import matplotlib.pyplot as pl

#%% linear regression
n_samples = 100

x = np.linspace(-1, 1, n_samples)
y = 3.2 * x + 1.4
y += np.random.randn(y.shape[0])

pl.plot(x, y, '.')

n_epoch = 100

class LinearModel:
    
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def predict(self, x):
        return self.a * x + self.b

a0 = -5
b0 = 5

learning_rate = 0.1
beta = 0.9

model = LinearModel(a0, b0)

for i in range(n_epoch):
    
    preds = model.predict(x)
    
    pl.cla()
    pl.plot(x, y, '.')
    pl.plot(x, preds)
    pl.ylim([min(y), max(y)])
    pl.pause(0.01)
    
    loss = np.sum(np.power(preds - y, 2))
    
    dl_da = np.mean( 2 * (model.a * x + model.b - y) * x )
    dl_db = np.mean( 2 * (model.a * x + model.b - y) * 1.0 )
    
    if i == 0:
        da = dl_da
        db = dl_db
    else:
        da = beta * dl_da + (1 - beta) * dl_da
        db = beta * dl_db + (1 - beta) * dl_db
    
    model.a -= learning_rate * da
    model.b -= learning_rate * db

#%% multiple linear regression

n_samples = 1000
n_features = 3

x = np.random.rand(n_samples, n_features)
x = np.hstack((
        np.ones((x.shape[0], 1)),
        x
    ))
beta = np.ones((n_features + 1, 1))
beta[0] = 1.0
beta[1] = 3.0
beta[2] = 2.0
y = np.matmul(x, beta)
y += np.random.randn(y.shape[0], 1)