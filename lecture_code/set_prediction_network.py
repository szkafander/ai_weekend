# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 17:45:00 2019

@author: tothp
"""
#%%
import numpy as np
from sklearn.datasets import make_blobs
import matplotlib.pyplot as pl
import tensorflow as tf

n_samples = 1000
n_centers = 4

x, y = make_blobs(n_samples=n_samples, centers=n_centers, n_features=2, random_state=6)

markers = ["bo", "ro", "go", "mo", "co", "yo"]
classes = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])

y_ = np.zeros((len(y), 2))

for i in range(n_centers):
    y_[y==i, :] = classes[i, :]
    
def smooth_max(x, alpha=5):
    return np.sum(x * np.exp(alpha * x)) / np.sum(np.exp(alpha * x))

def tf_smooth_max(x, alpha=5):
    return tf.reduce_sum(
            tf.divide(
                    tf.reduce_sum(x * tf.exp(alpha * x), axis=1, keep_dims=True),
                    tf.reduce_sum(tf.exp(alpha * x), axis=1, keep_dims=True)
                ),
            axis=1
        )

def tf_loss(output, permutations):
    s = tf.pow(tf.tile(tf.expand_dims(output, axis=-1), (1, 1, 2)) - permutations, 2).eval(session=tf.Session())
    s_sum = tf.reduce_sum(s, axis=2).eval(session=tf.Session())
    pass

test_logits = tf.constant(np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]]))
test_labels = tf.constant(np.array(
        [
            [[0.0, 0.0], [0.0, 0.0]],
            [[1.0, 1.0], [1.0, 1.0]],
            [[0.0, 1.0], [1.0, 0.0]],
            [[0.0, 1.0], [1.0, 0.0]]
        ]
    ))

for i in range(n_centers):
    pl.plot(x[y==i, 0], x[y==i, 1], markers[i])