# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 08:47:26 2019

@author: tothp
"""

#%% OLS for classification
import matplotlib.pyplot as pl
import numpy as np

from sklearn.datasets import make_classification

n_samples = 1000
n_input_features = 2

# generate data
x, y = make_classification(
        n_samples=n_samples,
        n_features=n_input_features, 
        n_classes=2,
        n_redundant=0, 
        n_informative=2,
        n_clusters_per_class=2,
        class_sep=0.5
    )

y = np.expand_dims(y, 1)

beta = np.matmul(np.linalg.inv(np.matmul(x.T, x)), np.matmul(x.T, y))

class Model:
    
    def predict(self, x):
        return np.matmul(x, beta)

from common import plot_preds

plot_preds(x, y, Model())