# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 22:51:30 2019

@author: tothp
"""

import numpy as np
import matplotlib.pyplot as pl

from typing import Any

def plot_preds(
        x: np.ndarray, 
        y: np.ndarray,
        model: Any
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
            np.flipud(np.reshape(preds.clip(0, 1), gx_0.shape)),
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