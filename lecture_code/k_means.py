# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 11:52:41 2019

@author: tothp
"""

#%%

import numpy as np
import matplotlib.pyplot as pl

from sklearn.datasets import make_blobs

n_samples = 1000
n_features = 2
n_centers = 4

# generate data
x, _ = make_blobs(
        n_samples=n_samples, 
        centers=n_centers, 
        n_features=n_features
    )

pl.plot(x[:,0], x[:,1], ".")

#%% k-means impementáció

from typing import List, Tuple

markers = ["bo", "rs", "g.", "y+", "m.", "cs"]

def k_means(
        x: np.array,
        k: int = 2, 
        n_iter: int = 100,
        plotting: bool = True
    ) -> Tuple[np.array, np.array]:

    random_index = np.random.choice(
            list(range(len(x))),
            size=k,
            replace=False
        )
    
    c = x[random_index, :]
    
    for i in range(n_iter):
        
        # indexelés
        distances = np.zeros((len(x), k))
        for k_ind in range(k):
            distances[:,k_ind] = np.sum(np.abs(x - np.tile(c[k_ind, :], (len(x), 1))), axis=1)
        
        labels = np.argmin(distances, axis=1)
        
        # centroidok ujraszamolasa
        for k_ind in range(k):
            x_in_label = x[labels==k_ind, :]
            c[k_ind, :] = np.mean(x_in_label, axis=0)
        
        # abrazolas
        if plotting:
            pl.cla()
            for k_ind in range(k):
                pl.plot(x[labels==k_ind, 0], x[labels==k_ind, 1], 
                        markers[k_ind])
                pl.plot(c[k_ind, 0], c[k_ind, 1], "k+")
            pl.pause(0.5)
            

    return c, labels

k_means(x, k=4, n_iter=100, plotting=True)

