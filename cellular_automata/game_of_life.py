# -*- coding: utf-8 -*-
import itertools
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as pl

from scipy import signal
from tensorflow.python.client import device_lib


#%% GOL test

flat_kernel = np.ones((3, 3))
neighborhood_kernel = np.array(
        [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]
        ]
    )

def get_no_of_live_neighbors(universe, mode='same', boundary='wrap'):
    return signal.convolve2d(
            universe, 
            neighborhood_kernel, 
            mode=mode, 
            boundary=boundary
        )

class GameOfLife:
    
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.shape = (w, h)
        self.universe = np.zeros((w, h))
        
    def initialize(self, probability_on):
        self.universe[np.random.rand(*self.shape) > probability_on] = 1
    
    def plot(self):
        pl.imshow(self.universe, interpolation='nearest')
        
    def step(self):
        live_cell = self.universe == 1
        nn = get_no_of_live_neighbors(self.universe)
        # rule 1
        rule_1 = nn < 2
        rule_2 = np.logical_or(nn == 2, nn == 3)
        rule_3 = nn > 3
        rule_4 = nn == 3
        self.universe[np.logical_and(live_cell, rule_1)] = 0
        self.universe[np.logical_and(live_cell, rule_2)] = 1
        self.universe[np.logical_and(live_cell, rule_3)] = 0
        self.universe[np.logical_and(np.logical_not(live_cell), rule_4)] = 1
        
        
gol = GameOfLife(111, 111)
gol.initialize(0.8)

for i in range(1000):
    pl.cla()
    gol.plot()
    gol.step()
    pl.pause(0.01)
    
    
#%% all x
    
inds = np.arange(0, 9)

def all_combinations(iterable):
    n = len(iterable)
    combs_ = []
    for n_ in range(n+1):
        combs = itertools.combinations(iterable, n_)
        for comb in combs:
            combs_.append(comb)
    return combs_

def ind2sub(array_shape, ind):
    ind[ind < 0] = -1
    ind[ind >= array_shape[0]*array_shape[1]] = -1
    rows = (ind.astype('int') / array_shape[1])
    cols = ind % array_shape[1]
    return (rows, cols)

all_ind_combs = all_combinations([0, 1, 2, 3, 4, 5, 6, 7, 8])

x = np.zeros((512, 3, 3))
for k, comb in enumerate(all_ind_combs):
    x_current = x[k, :, :]
    if len(comb) > 0:
        i, j = np.unravel_index(comb, (3, 3))
        x_current[i, j] = 1
        
x = np.expand_dims(x, axis=-1)
        
#%% compute all y
        
y = np.zeros((512,))

for i in range(512):
    x_current = x[i, :, :, 0]
    
    y_ = 0
    
    live_cell = x_current[1, 1] == 1
    nn = get_no_of_live_neighbors(x_current, mode='valid')[0][0]
    # rule 1
    rule_1 = nn < 2
    rule_2 = nn == 2 or nn == 3
    rule_3 = nn > 3
    rule_4 = nn == 3
    if live_cell and rule_1:
        y_ = 0
    if live_cell and rule_2:
        y_ = 1
    if live_cell and rule_3:
        y_ = 0
    if not live_cell and rule_4:
        y_ = 1
    
    y[i] = y_

y = y[:, np.newaxis, np.newaxis, np.newaxis]

#%% visualize to check
    
inds = np.random.choice(range(512), 100, replace=False)
for i, k in enumerate(inds):
    pl.subplot(10, 10, i+1)
    pl.imshow(x[k, :, :, 0])
    pl.title(str(y[k, 0, 0, 0]))
    pl.xticks([])
    pl.yticks([])
    

#%% make model

    
input_tensor = tf.keras.layers.Input((None, None, 1))

z_1 = tf.keras.layers.Conv2D(2, (3, 3))(input_tensor)
a_1 = tf.keras.layers.Activation("relu")(z_1)

z_2 = tf.keras.layers.Conv2D(3, (1, 1))(a_1)
a_2 = tf.keras.layers.Activation("relu")(z_2)

z_3 = tf.keras.layers.Conv2D(1, (1, 1))(a_2)
a_3 = tf.keras.layers.Activation("sigmoid")(z_3)

model = tf.keras.models.Model(inputs=[input_tensor], outputs=[a_3])
model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.005), loss="binary_crossentropy", metrics=["binary_accuracy"])

model.fit(x=x, y=y, batch_size=512, epochs=10000)

#%% evaluate

preds = model.predict(x)

inds = np.random.choice(range(512), 100, replace=False)
for i, k in enumerate(inds):
    pl.subplot(10, 10, i+1)
    pl.imshow(x[k, :, :, 0])
    pl.title("true: " + str(y[k, 0, 0, 0]) + "pred: " + str(int(np.round(preds[k, 0, 0, 0]))))
    pl.xticks([])
    pl.yticks([])

pl.figure()
pl.plot(y[:, 0, 0, 0], preds[:, 0, 0, 0], 'o')
    
#%%
    
gol = GameOfLife(128, 128)
gol.initialize(0.8)
universe = gol.universe
k = 0
kk = 0

for k in range(5000):
    if k == 0:
        out = np.pad(universe, 1, 'wrap')[np.newaxis, :, :, np.newaxis]
    else:
        out = np.pad(out[0,:,:,0], 1, 'wrap')[np.newaxis, :, :, np.newaxis]
    
    out = np.round(model.predict(out))
    
    pl.cla()
    pl.imshow(out[0,:,:,0])
    pl.pause(0.01)
    
#    print("predicted {}".format(k))
#    if k % 50 == 0:
#        kk += 1
#        pl.subplot(1, 10, kk)
#        pl.imshow(out[0, :, :, 0])