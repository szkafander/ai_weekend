# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 23:07:44 2019

@author: tothp
"""
#%%
import numpy as np
import tensorflow as tf

from sklearn.datasets import make_moons

n_samples = 1000
n_features = 1

x_, _ = make_moons(
        n_samples=n_samples,
        noise=0.1
    )

y = x_[:, 0:1]
x = x_[:, 1:2]

y = np.linspace(-1, 1, n_samples)
x = np.sin(y * 4)
x += np.random.randn(*x.shape) * 0.2

x = np.expand_dims(x, -1)
y = np.expand_dims(y, -1)


x -= x.mean()
x /= x.std()
y -= y.mean()
y /= y.std()

output_tensor = tf.constant(y, dtype=tf.float32)

n_hidden = 50
n_outputs = 1

n_mixture = 4

def sample_predictions(pi_vals, mu_vals, var_vals, samples=10):
    n, k = pi_vals.shape
    # print('shape: ', n, k, l)
    # place holder to store the y value for each sample of each row
    out = np.zeros((n, samples, n_outputs))
    for i in range(n):
        for j in range(samples):
            # for each sample, use pi/probs to sample the index
            # that will be used to pick up the mu and var values
            idx = np.random.choice(range(k), p=pi_vals[i])
            for li in range(n_outputs):
                # Draw random sample from gaussian distribution
                out[i,j,li] = np.random.normal(mu_vals[i, idx*(li+n_outputs)], var_vals[i, idx])
    return out

w_hidden = tf.Variable(tf.random_normal([n_features, n_hidden]), name="w_hidden")
b_hidden = tf.Variable(tf.random_normal([n_hidden]), name="b_hidden")

w_mu = tf.Variable(tf.random_normal([n_hidden, n_mixture * n_outputs]), name="w_mu")
b_mu = tf.Variable(tf.random_normal([n_mixture * n_outputs]), name="b_mu")

w_var = tf.Variable(tf.random_normal([n_hidden, n_mixture * n_outputs]), name="w_var")
b_var = tf.Variable(tf.random_normal([n_mixture * n_outputs]), name="b_var")

w_pi = tf.Variable(tf.random_normal([n_hidden, n_mixture * n_outputs]), name="w_pi")
b_pi = tf.Variable(tf.random_normal([n_mixture * n_outputs]), name="b_pi")

input_tensor = tf.placeholder(tf.float32, shape=(None, n_features))
hidden = tf.nn.tanh(tf.add(tf.matmul(input_tensor, w_hidden), b_hidden))
mu = tf.add(tf.matmul(hidden, w_mu), b_mu)
var = tf.add(tf.nn.elu(tf.add(tf.matmul(hidden, w_var), b_var)), 1 + 1e-7)
pi = tf.nn.softmax(tf.add(tf.matmul(hidden, w_pi), b_pi))

optimizer = tf.train.AdamOptimizer(learning_rate=0.005)

oneDivSqrtTwoPI = 1 / np.sqrt(2*np.pi)

def tf_normal(y, mu_, var_):
    result = tf.subtract(y, mu_)
    result = tf.multiply(result, tf.reciprocal(var_))
    result = -tf.square(result) / 2
    return tf.multiply(tf.exp(result), tf.reciprocal(var_)) * oneDivSqrtTwoPI


def get_lossfunc(y, out_pi, out_mu, out_sigma):
    result = tf_normal(y, out_mu, out_sigma)
    result = tf.multiply(result, out_pi)
    result = tf.reduce_sum(result, 1, keep_dims=True)
    result = - tf.log(result + 1e-10)
    return tf.reduce_mean(result)

loss = get_lossfunc(output_tensor, pi, mu, var)
train_op = optimizer.minimize(loss)


n_epochs = 5000

losses = []

sess = tf.Session()

sess.run(tf.global_variables_initializer())

for i in range(n_epochs):
    
    _, l, mu_, var_, pi_ = sess.run(
            [train_op, loss, mu, var, pi],
            feed_dict={
                    input_tensor: x
                }
            )
    
    if not np.isnan(l):
        mu__ = mu_
        var__ = var_
        pi__ = pi_
        losses.append(l)
    else:
        break
    
    if i % 10 == 0:
        s = sample_predictions(pi_, mu_, var_, 1)
        s = s[:, :, 0]
        
        pl.subplot(1, 2, 1)
        pl.cla()
        pl.plot(x, y, '.')
        pl.plot(x, s, '+')
        pl.xlim([-2, 2])
        pl.ylim([-2, 2])
        
        pl.subplot(1, 2, 2)
        pl.cla()
        pl.semilogy(losses)
        pl.pause(0.01)

predict = lambda x: sess.run([pi, mu, var], feed_dict={input_tensor: x})
#%%
[p_, m_, v_] = predict(x)

pl.plot(x, y, '.')
for m in m_.T:
    pl.plot(x.flatten(), m, '+')

#%%
def sample_predictions(pi_vals, mu_vals, var_vals, samples=10):
    n, k = pi_vals.shape
    # print('shape: ', n, k, l)
    # place holder to store the y value for each sample of each row
    out = np.zeros((n, samples, n_outputs))
    for i in range(n):
        for j in range(samples):
            # for each sample, use pi/probs to sample the index
            # that will be used to pick up the mu and var values
            idx = np.random.choice(range(k), p=pi_vals[i])
            for li in range(n_outputs):
                # Draw random sample from gaussian distribution
                out[i,j,li] = np.random.normal(mu_vals[i, idx*(li+n_outputs)], var_vals[i, idx])
    return out

s = sample_predictions(p_, m_, v_, 1)
s = s[:, :, 0]

pl.plot(x, y, '.')
pl.plot(x, s, '+')