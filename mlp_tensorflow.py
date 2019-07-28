# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 15:38:06 2019

@author: tothp
"""
#%%
import tensorflow as tf

import matplotlib.pyplot as pl
import numpy as np
import common

from sklearn.datasets import make_moons

n_samples = 100
n_input_features = 2
n_output_features = 1

# generate data
x, y = make_moons(
        n_samples=n_samples,
        noise=0.15
    )

y = np.expand_dims(y, 1)

for i in range(2):
    pl.plot(x[(y==i).flatten(), 0], x[(y==i).flatten(), 1], markers[i])
    
#%%

n_hidden = 20

input_layer = tf.placeholder(dtype=tf.float32, shape=(None, 2), name="input_layer")
output_layer = tf.placeholder(dtype=tf.float32, shape=(None, 1), name="output_layer")

w_hidden = tf.Variable(tf.random_normal([n_input_features, n_hidden]), name="w_hidden")
w_output = tf.Variable(tf.random_normal([n_hidden, n_output_features]), name="w_output")

b_hidden = tf.Variable(tf.random_normal([n_hidden]), name="b_hidden")
b_output = tf.Variable(tf.random_normal([n_output_features]), name="b_output")

a_hidden = tf.nn.sigmoid(tf.add(tf.matmul(input_layer, w_hidden), b_hidden), name="a_hidden")
a_output = tf.nn.sigmoid(tf.add(tf.matmul(a_hidden, w_output), b_output), name="a_output")

loss = tf.losses.mean_squared_error(output_layer, a_output)

optimizer = tf.train.GradientDescentOptimizer(learning_rate=1.0)

train_op = optimizer.minimize(loss)

n_epochs = 10000

sess = tf.Session()

sess.run(tf.global_variables_initializer())

losses = []

class Model:
    
    def __init__(self, tensor):
        self.tensor = tensor
        
    def predict(self, x):
        output = sess.run(self.tensor, feed_dict={input_layer: x})
        return output

model = Model(a_output)

for i in range(n_epochs):
    
    _, loss_ = sess.run(
            [train_op, loss],
            feed_dict={
                    input_layer: x, 
                    output_layer: y
                }
        )
    
    losses.append(loss_)
    
    if i % 100 == 0:
        pl.subplot(1,2,1)
        pl.cla()
        pl.plot(losses)
        pl.pause(0.01)
    
        pl.subplot(1,2,2)
        pl.cla()
        common.plot_preds(x, y, model)

#%% multilayer perceptron
import matplotlib.pyplot as pl
import numpy as np

tf.reset_default_graph()

n_input_features = 1
n_output_features = 1
n_samples = 200

x = np.random.rand(n_samples, 1) * 2.0 - 1.0
x.sort(axis=0)
y = x ** 2 + np.sin(x * 15) * 0.25
y -= np.mean(y)
y /= np.std(y)

y += np.random.randn(*y.shape) * 0.1


n_hidden = 300

input_layer = tf.placeholder(dtype=tf.float32, shape=(None, n_input_features), name="input_layer")
output_layer = tf.placeholder(dtype=tf.float32, shape=(None, n_output_features), name="output_layer")

w_hidden = tf.Variable(tf.random_normal([n_input_features, n_hidden]), name="w_hidden")
w_output = tf.Variable(tf.random_normal([n_hidden, n_output_features]), name="w_output")

b_hidden = tf.Variable(tf.random_normal([n_hidden]), name="b_hidden")
b_output = tf.Variable(tf.random_normal([n_output_features]), name="b_output")

a_hidden = tf.nn.tanh(tf.add(tf.matmul(input_layer, w_hidden), b_hidden), name="a_hidden")
a_output = tf.add(tf.matmul(a_hidden, w_output), b_output, name="a_output")

loss = tf.losses.mean_squared_error(output_layer, a_output)

optimizer = tf.train.AdamOptimizer(learning_rate=0.01)

train_op = optimizer.minimize(loss)

n_epochs = 10000

sess = tf.Session()

writer = tf.summary.FileWriter("C:\\projects\\education\\deep_learning\\code\\logs",
                               sess.graph)

sess.run(tf.global_variables_initializer())

losses = []

loss_summary = tf.summary.scalar(name="loss_summary", tensor=loss)
merged = tf.summary.merge_all()


for i in range(n_epochs):
    
    _, loss_, a_output_, summary_ = sess.run(
            [train_op, loss, a_output, merged],
            feed_dict={
                    input_layer: x, 
                    output_layer: y
                }
        )
    
    writer.add_summary(summary_, i)
    
    losses.append(loss_)

    if i % 100 == 0:
        pl.subplot(1,2,1)
        pl.cla()
        pl.plot(losses)
        pl.pause(0.01)
    
        pl.subplot(1,2,2)
        pl.cla()
        pl.plot(x, y, 'ro')
        pl.plot(x, a_output_, "b")
        
        
#%% keras
        
from tensorflow import keras

n_hidden = 30

model = keras.Sequential([
            keras.layers.Dense(n_hidden, activation="sigmoid"),
            keras.layers.Dense(n_output_features, activation="linear")
        ])

model.compile(keras.optimizers.Adam(lr=0.01), loss="mse")

model.fit(x, y, epochs=10000, callbacks=[keras.callbacks.History()], verbose=2)

preds = model.predict(x)

pl.plot(x, y, "ro")
pl.plot(x, preds)

#%%
# linear classification

import numpy as np
import matplotlib.pyplot as pl
import common

from sklearn.datasets import make_classification
from typing import Callable

from tensorflow import keras

n_samples = 1000
n_classes = 2
n_input_features = 2
n_output_features = 1

#x, y = make_classification(
#        n_samples=n_samples,
#        n_features=n_input_features,
#        n_classes=n_classes,
#        n_redundant=0,
#        n_informative=2,
#        n_clusters_per_class=2,
#        class_sep=2.5
#    )

#y = np.expand_dims(y, 1)

n_hidden = 5
    
l2_weight = 0.001

input_layer = keras.layers.Input((2,))
hidden_layer = keras.layers.Dense(
        n_hidden, 
        activation="tanh",
        kernel_regularizer=keras.regularizers.l1(l2_weight)
    )(input_layer)
output_layer = keras.layers.Dense(
        n_output_features, 
        activation="sigmoid",
        kernel_regularizer=keras.regularizers.l1(l2_weight)
    )(hidden_layer)

model = keras.models.Model(inputs=[input_layer], outputs=[output_layer])

model.compile(keras.optimizers.Adam(lr=0.01), loss="mse")

n_epochs = 10000

for i in range(n_epochs):
    
    model.train_on_batch(x, y)
    
    if i % 100 == 0:
        pl.cla()
        common.plot_preds(x, y, model)
        pl.pause(0.01)
