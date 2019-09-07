# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 17:58:36 2019

@author: tothp
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 21:09:58 2019

@author: tothp
"""

#%% multilayer perceptron
import matplotlib.pyplot as pl
import numpy as np

n_samples = 200

x = np.random.rand(n_samples, 1) * 2.0 - 1.0
x.sort(axis=0)
y = x ** 2 + np.sin(x * 15) * 0.25
y -= np.mean(y)
y /= np.std(y)

y += np.random.randn(*y.shape) * 0.1

#%% perceptron class

tanh = lambda x: (2 / (1 + np.exp(-2 * x))) - 1
d_tanh_dx = lambda x: 1 - tanh(x) ** 2

class MLP:
    
    def __init__(
            self, 
            n_features: int = 2,
            n_hidden: int = 50,
            n_outputs: int = 1
        ) -> None:
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.weights_hidden = np.random.randn(n_features + 1, n_hidden)
        self.weights_output = np.random.randn(n_hidden + 1, n_outputs)
        self.activations_hidden = "uninitialized"
        self.activations_output = "uninitialized"
        self.out_input = "uninitialized"
        self.out_hidden = "uninitialized"
        self.out_output = "uninitialized"
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        self.out_input = np.hstack((x, np.ones((x.shape[0], 1))))
        self.activations_hidden = np.matmul(
                self.out_input, 
                self.weights_hidden)
        self.out_hidden = np.hstack(
                (
                    tanh(self.activations_hidden),
                    np.ones((x.shape[0], 1))
                )
            )
        self.activations_output = np.matmul(
                self.out_hidden, 
                self.weights_output
            )
        self.out_output = self.activations_output
        return self.out_output
    
    def train(self, x: np.ndarray, y: np.ndarray) -> None:
        pass

# plot data
def plot_preds(
        x: np.ndarray, 
        y: np.ndarray,
        model: MLP
    ) -> None:
    
    pl.cla()
    pl.plot(x, y, "ro")
    pl.plot(x, model.predict(x), "g")

n_epochs = 100000
learning_rate = 0.075

mlp = MLP(n_features=1, n_hidden=20, n_outputs=1)

#pl.subplot(1, 2, 1)
#plot_preds(x, y, perceptron)

y_ = y.ravel()

for i in range(n_epochs):
    
    # forward pass
    output = mlp.predict(x)
    
    # error
    error = output - y
    
    # gradient
    delta_w_output = np.matmul(
            mlp.out_hidden.T, 
            2 * error * 1
        )
    delta_w_hidden = np.matmul(
            mlp.out_input.T,
            np.matmul(
                    2 * error * 1,
                    mlp.weights_output.T[:, :-1]
                ) * d_tanh_dx(mlp.activations_hidden)
            )
    
    # descend
    mlp.weights_hidden -= 1/n_samples * learning_rate * delta_w_hidden
    mlp.weights_output -= 1/n_samples * learning_rate * delta_w_output
    
    if i % 3000 == 0:
        plot_preds(x, y, mlp)
        pl.pause(0.01)

#pl.subplot(1, 2, 2)
#plot_preds(x, y, perceptron)