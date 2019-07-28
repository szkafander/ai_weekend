# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 22:14:10 2019

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

input_tensor = tf.placeholder(tf.float32, shape=(None, 2), name="input")
output_tensor = tf.placeholder(tf.float32, shape=(None, 1), name="output")

weights_hidden = tf.Variable(tf.random_normal([n_features, n_hidden]), name="w_hidden")
biases_hidden = tf.Variable(tf.random_normal([n_hidden]), name="b_hidden")

weights_out = tf.Variable(tf.random_normal([n_hidden, n_outputs]), name="w_out")
biases_out = tf.Variable(tf.random_normal([n_outputs]), name="b_out")

layer_hidden = tf.nn.sigmoid(tf.add(tf.matmul(input_tensor, weights_hidden, name="x_dot_w_hidden"), biases_hidden, name="z_hidden_plus_b_hidden"), name="g_hidden_z_hidden")
layer_out = tf.nn.sigmoid(tf.add(tf.matmul(layer_hidden, weights_out, name="a_hidden_dot_w_out"), biases_out, name="z_out_plus_b_out"), name="g_out_z_out")

loss = tf.losses.mean_squared_error(output_tensor, layer_out)
        
optimizer = tf.train.GradientDescentOptimizer(learning_rate=1)

train_op = optimizer.minimize(loss)

n_epochs = 10000

losses = []

sess = tf.Session()

sess.run(tf.global_variables_initializer())

for i in range(n_epochs):
    
    _, l = sess.run(
            [train_op, loss],
            feed_dict={
                    input_tensor: x,
                    output_tensor: y
                }
            )
    
    losses.append(l)
        
pl.subplot(1, 2, 1)
pl.plot(losses)

min_x_0 = min(x[:,0])
max_x_0 = max(x[:,0])
min_x_1 = min(x[:,1])
max_x_1 = max(x[:,1])

gx_0, gx_1 = np.meshgrid(
        np.linspace(min_x_0, max_x_0, 50),
        np.linspace(min_x_1, max_x_1, 50)
    )

gx = np.c_[gx_0.ravel(), gx_1.ravel()]

preds = layer_out.eval(feed_dict={input_tensor: gx}, session=sess)

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