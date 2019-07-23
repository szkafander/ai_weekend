# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 17:40:01 2019

@author: tothp
"""

#%% extreme learning machine
import matplotlib.pyplot as pl
import numpy as np

from common import plot_preds
from sklearn.datasets import make_classification

n_samples = 1000
n_features = 2

# generate data
x, y = make_classification(
        n_redundant=0,
        n_clusters_per_class=1,
        n_features=n_features,
        n_samples=n_samples
    )

y = np.expand_dims(y, -1)

# can we just least-square it?
beta = np.matmul(
        np.linalg.inv(np.matmul(x.T, x)), 
        np.matmul(x.T, y)
    )

lsq_predict = lambda x: np.matmul(x, beta)

class LSQ:
    
    def predict(self, x):
        return lsq_predict(x)
    
plot_preds(x, y, LSQ())

#%%

sigmoid = lambda x: 1 / (1 + np.exp(-x))

def layer_op(input_, w, g):
    return g(np.matmul(input_, w))

sparsity_threshold = 0.5
n_hidden = 30

w_hidden_1 = np.random.randn(n_features, n_hidden)
w_hidden_1[np.random.rand(*w_hidden_1.shape) < sparsity_threshold] = 0

w_hidden_2 = np.random.randn(n_hidden, n_hidden)
w_hidden_2[np.random.rand(*w_hidden_2.shape) < sparsity_threshold] = 0

elm_reservoir = lambda x: layer_op(layer_op(x, w_hidden_1, sigmoid), w_hidden_2, sigmoid)

a_reservoir = elm_reservoir(x)

beta = np.matmul(
        np.linalg.inv(np.matmul(a_reservoir.T, a_reservoir)), 
        np.matmul(a_reservoir.T, y)
    )

elm_predict = lambda x: np.matmul(elm_reservoir(x), beta)

class ELM:
    
    def predict(self, x):
        return elm_predict(x)
    
elm = ELM()



plot_preds(x, y, elm)