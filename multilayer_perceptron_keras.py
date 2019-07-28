# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 23:18:15 2019

@author: tothp
"""

#%%
import matplotlib.pyplot as pl
import numpy as np
import tensorflow as tf

from sklearn.datasets import make_moons

n_samples = 100
n_features = 2

# generate data
x, y = make_moons(
        n_samples=n_samples,
        noise=0.1
    )

y = np.expand_dims(y, -1)

n_hidden = 10
n_outputs = 1

model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(n_hidden),
            tf.keras.layers.Activation("sigmoid"),
            tf.keras.layers.Dense(n_outputs),
            tf.keras.layers.Activation("sigmoid")
        ]
    )

model.compile(tf.keras.optimizers.SGD(lr=1), loss="mse")
history = model.fit(
        x, 
        y, 
        epochs=10000, 
        verbose=0, 
        callbacks=[tf.keras.callbacks.History()]
    )

pl.subplot(1, 2, 1)
pl.plot(history.history["loss"])

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

pl.subplot(1, 2, 2)
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