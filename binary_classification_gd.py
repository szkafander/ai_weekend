# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 10:57:13 2019

@author: tothp
"""
#%%
# linear classification

import numpy as np
import matplotlib.pyplot as pl
import common

from sklearn.datasets import make_classification
from typing import Callable

n_samples = 1000
n_classes = 2
n_input_features = 2

x, y = make_classification(
        n_samples=n_samples,
        n_features=n_input_features,
        n_classes=n_classes,
        n_redundant=0,
        n_informative=2,
        n_clusters_per_class=2,
        class_sep=2.5
    )

y = np.expand_dims(y, 1)

markers = ["ro", "bo", "go", "yo", "mo", "co"]
#%%
pl.figure()
for i in range(n_classes):
    pl.plot(x[(y==i).flatten(), 0], x[(y==i).flatten(), 1], markers[i])
    
    
#%%
    
def identity(x):
    return x

def identity_prime(x):
    return np.ones(x.shape)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))

class ActivationFunction:
    
    def __init__(self, function: Callable, derivative: Callable) -> None:
        self.function = function
        self.derivative = derivative

identity_activation = ActivationFunction(identity, identity_prime)
sigmoid_activation = ActivationFunction(sigmoid, sigmoid_prime)

def mse(y_hat, y):
    return np.sum((y_hat - y) ** 2)
    
class Model:
    
    def __init__(
            self, 
            n_features: int = 2, 
            n_outputs: int = 1, 
            g: ActivationFunction = identity_activation
        ) -> None:
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.w_1 = np.random.randn(n_features + 1, n_outputs)
        self.w_2 = np.random.randn(n_features + 1, n_outputs)
        self.g = g
        self.z_1 = None
        self.a_1 = None
        self.z_2 = None
        self.a_2 = None
        
    def predict(self, x: np.ndarray) -> np.ndarray:
        
        # forward pass
        
        # input layer
        x_with_1s = np.hstack( (x, np.ones( (x.shape[0], 1) ) ) )
        
        self.z_1 = np.matmul(x_with_1s, self.w_1) # np.sum(x * w)
        self.a_1 = self.g.function(self.z_1)
        
        # hidden layer
        a_1_with_1s = np.hstack( (self.a_1, np.ones( (x.shape[0], 1) ) ) )
        
        self.z_2 = np.matmul(a_1_with_1s, self.w_2)
        self.a_2 = self.g.function(self.z_2)
        
        return self.a_2
    
    def train(
            self, 
            x: np.ndarray, 
            y: np.ndarray, 
            learning_rate: float = 0.001,
            n_epochs: int = 1000
        ) -> None:
        
        x_with_1s = np.hstack( (x, np.ones( (x.shape[0], 1) ) ) )
        
        for i in range(n_epochs):
            # forward pass
            y_hat = self.predict(x)
            
            error = y_hat - y
            
            # backward pass
            
            # output layer
            a_2_with_1s = np.hstack( (self.a_2, np.ones( (x.shape[0], 1) ) ) )
            g_prime_at_z = self.g.derivative(self.z)
            p_l_p_w_1 = np.matmul( a_2_with_1s.T, g_prime_at_z * 2 * error ) )
            
            # hidden layer
            p_l_p_w_2 = np.matmul( self.w_2, g_prime_at_z * 2 * error )
            
            
            self.w_1 += - learning_rate * p_l_p_w_1 * (1 / x.shape[0])
            if i % 100 == 0:
                pl.cla()
                common.plot_preds(x, y, self)
                pl.pause(0.01)
    
    
model = Model(g=sigmoid_activation)
pl.figure()
model.train(x, y, n_epochs=10000, learning_rate=0.005)
    
    
    