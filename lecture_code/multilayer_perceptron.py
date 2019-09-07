# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 21:09:58 2019

@author: tothp
"""

#%% multilayer perceptron
import matplotlib.pyplot as pl
import numpy as np

from sklearn.datasets import make_moons

n_samples = 100
n_input_features = 2

# generate data
x, y = make_moons(
        n_samples=n_samples,
        noise=0.1
    )

y = np.expand_dims(y, 1)

#%% perceptron class
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
                self.weights_hidden
            )
        self.out_hidden = np.hstack(
                (
                    sigmoid(self.activations_hidden),
                    np.ones((x.shape[0], 1))
                )
            )
        self.activations_output = np.matmul(
                self.out_hidden, 
                self.weights_output
            )
        self.out_output = sigmoid(self.activations_output)
        return self.out_output
    
    def train(self, x: np.ndarray, y: np.ndarray) -> None:
        pass

# plot data
def plot_preds(
        x: np.ndarray, 
        y: np.ndarray,
        model: MLP
    ) -> None:
    
    min_x_0 = min(x[:,0])
    max_x_0 = max(x[:,0])
    min_x_1 = min(x[:,1])
    max_x_1 = max(x[:,1])
    
    gx_0, gx_1 = np.meshgrid(
            np.linspace(min_x_0, max_x_0, 50),
            np.linspace(min_x_1, max_x_1, 50)
        )
    
    gx = np.c_[gx_0.ravel(), gx_1.ravel()]
    
    preds = model.predict(gx)
    
    pl.imshow(
            np.flipud(np.reshape(preds, gx_0.shape)),
            extent=[min_x_0, max_x_0, min_x_1, max_x_1]
        )
    
    y_ = y.flatten()
    
    pl.plot(
            x[y_==0, 0],
            x[y_==0, 1],
            "o"
        )
    pl.plot(
            x[y_==1, 0],
            x[y_==1, 1],
            "o"
        )

sigmoid = lambda x: 1 / (1 + np.exp(-x))
d_sigmoid_d_x = lambda x: sigmoid(x) * (1 - sigmoid(x))

n_epochs = 100000
learning_rate = 1

mlp = MLP(n_features=2, n_hidden=100, n_outputs=1)

losses = []

losses_val = []

#pl.subplot(1, 2, 1)
#plot_preds(x, y, perceptron)

y_ = y.ravel()

for i in range(n_epochs):
    
    if i % 500 == 0:
        pl.subplot(1,2,1)
        pl.cla()
        plot_preds(x, y, mlp)
        pl.pause(0.01)
    
    # forward pass
    x_augmented = x + np.random.randn(*x.shape) * 0.01
    output = mlp.predict(x_augmented)
    
    # error
    error = output - y
    
    # gradient
    delta_w_output = np.matmul(
            mlp.out_hidden.T, 
            2 * error * d_sigmoid_d_x(mlp.activations_output)
        )
    delta_w_hidden = np.matmul(
            mlp.out_input.T,
            np.matmul(
                    2 * error * d_sigmoid_d_x(mlp.activations_output),
                    mlp.weights_output.T[:, :-1]
                ) * d_sigmoid_d_x(mlp.activations_hidden)
            )
    
    # descend
    mlp.weights_hidden -= 1/n_samples * learning_rate * delta_w_hidden
    mlp.weights_output -= 1/n_samples * learning_rate * delta_w_output
    
    loss = np.mean(error ** 2)
    losses.append(loss)
    
    loss_val = np.mean( (mlp.predict(x_val) - y_val) ** 2 )
    losses_val.append(loss_val)
    
    if i % 500 == 0:
        pl.subplot(1,2,2)
        pl.cla()
        pl.plot(losses)
        pl.plot(losses_val)
    

#pl.subplot(1, 2, 2)
#plot_preds(x, y, perceptron)