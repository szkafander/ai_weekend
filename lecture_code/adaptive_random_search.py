# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 15:41:46 2019

@author: tothp
"""

#%%

import numpy as np
import matplotlib.pyplot as pl

n_samples = 100

x = np.linspace(-1, 1, n_samples)

y = lambda x: np.sin(x*25) * 0.5 + x ** 2


n_tries = 100

def get_x_tries(search_min, search_max, n_tries):
    return np.random.rand(n_tries) * (search_max - search_min) + search_min

n = 5
n_iter = 10

lower_range, upper_range = -1, 1

for _ in range(n_iter):
    # x helyek
    x_tries = get_x_tries(lower_range, upper_range, n_tries)
    # y értéke az x helyeken
    y_tries = y(x_tries)
    # x értéke a minimális y-nál az y_tries-ból
    ind_sorted_y = np.argsort(y_tries)
    y_min_n = y_tries[ind_sorted_y][:n]
    x_min_n_y = x_tries[ind_sorted_y][:n]
    lower_range = x_min_n_y.min()
    upper_range = x_min_n_y.max()
    # plot
    pl.cla()
    pl.plot(x, y(x), "b")
    pl.plot(x_tries, y(x_tries), 'r.')
    pl.pause(0.5)

# pseudorandom numbers
# latin hypercube sampling
# sobol sequences

