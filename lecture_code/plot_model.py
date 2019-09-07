# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 23:51:43 2019

@author: tothp
"""
#%%
from tensorflow import keras

input_layer = keras.layers.Input(shape=(2,))
output_layer = keras.layers.Dense(25)(input_layer)
output_layer = keras.layers.Dense(1)(output_layer)

model = keras.models.Model(inputs=[input_layer], outputs=[output_layer])

keras.utils.plot_model(model, "test.png", show_shapes=True)