# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 23:41:05 2019

@author: tothp
"""
import numpy as np
from scipy import signal

from typing import Optional


dirichlet_kernel = np.array([[0, 1, 0],
                             [1, 0, 1],
                             [0, 1, 0]])

neumann_kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

default_kernel = dirichlet_kernel


def material_props_from_file(filename: str) -> dict:
    """ Reads mat props from file and returns a dict. """
    pass


def probabilities(temperature: float) -> None:
    """ Pull mat props into np array, apply Arrhenius formula vectorized, then fill
    probabilities dict. """
    pass


def enforce_boundaries(field: np.ndarray) -> np.ndarray:
    """ Enforces the periodic BC on field and returns a new field. """
    return np.pad(field, 1, 'wrap')


# methods that act on binary fields
# -----------------------------------------------------------------------------
def count_live_neighbors(
        field: np.ndarray,
        kernel: Optional[np.ndarray] = None,
        mode: str = "same",
        boundary: str = "wrap"
    ) -> np.ndarray:
    """ Counts the neighbors with 'on' values. """
    kernel = kernel or default_kernel
    return signal.convolve2d(
            field,
            kernel,
            mode=mode,
            boundary=boundary
        )


# TODO - factor out shared matrices if needed
def count_same_neighbors(
        field: np.ndarray,
        kernel: Optional[np.ndarray] = None,
        mode: str = "same",
        boundary: str = "wrap"
    ) -> np.ndarray:
    """ Counts the neighbors with the same values as the center pixel. """
    kernel = kernel or default_kernel
    n_neighbors = count_live_neighbors(field, kernel, mode, boundary)
    n_off_neighbors = kernel.sum() - n_neighbors
    n_neighbors[field == 0] = n_off_neighbors[field == 0]
    return n_neighbors


def count_different_neighbors(
        field: np.ndarray,
        kernel: Optional[np.ndarray] = None,
        mode: str = "same",
        boundary: str = "wrap"
    ) -> np.ndarray:
    """ Counts the neighbors with the opposite values as the center pixel. """
    kernel = kernel or default_kernel
    n_neighbors = count_live_neighbors(field, kernel, mode, boundary)
    n_off_neighbors = kernel.sum() - n_neighbors
    n_neighbors[field == 1] = n_off_neighbors[field == 1]
    return n_neighbors


# this can be fully vectorized
def allotropic_nucleation(
        phase_field: np.ndarray,
        deformed_field: np.ndarray,
        probabilities: dict,
        material: dict,
        temperature: float
    ) -> np.ndarray:
    """ Automata::AllotropicNucleation; returns newarray. """
    pass


def recrystallisation_nucleation(): pass


def allotropic_growth(): pass


def recrystallisation_growth(): pass


def grain_coarsening(): pass


# TODO - find shared matrices and refactor
def step(): pass
