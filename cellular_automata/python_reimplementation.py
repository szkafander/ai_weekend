# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 23:41:05 2019

@author: tothp
"""
import numpy as np

from scipy import signal
from tabulate import tabulate
from typing import Optional, Tuple, Union


dirichlet_kernel = np.array([[0, 1, 0],
                             [1, 0, 1],
                             [0, 1, 0]])

neumann_kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]])

default_kernel = dirichlet_kernel


# methods related to reading material properties
# -----------------------------------------------------------------------------
# these are the category names
CATS = ("Material", "PHASE0", "PHASE1", "Process", "Structure")

def _clear_string(string: str) -> str:
    return string.strip().replace("[", "").replace("]", "")


def _parse_line(line: str) -> Tuple:
    return _clear_string(line).split("\t")


def read_constants(filename: str) -> dict:
    """ Reads constant props into nested dict {category: {property: value}}. 
    The text file should be properly formatted. The first line should be a 
    category name. """
    constants = {}
    f = open(filename)
    for k, line in enumerate(f):
        parsed = _parse_line(line)
        n = len(parsed)
        if n == 1:
            category, = parsed
            if category not in constants:
                constants[category] = {}
        elif n == 2:
            if k == 0:
                raise ValueError("The first line should be a category.")
            prop, value = parsed
            constants[category].update({prop: value})
        else:
            raise ValueError("Invalid parsed line {}".format(parsed))
    return constants


# methods related to updating probabilities
# -----------------------------------------------------------------------------
# these are the order of property names for vectorized Arrhenius rate calc
MATERIAL_PROPS = ("Tall", "Qallg", "Ballg", "Estor")
PHASE_PROPS = ("Qrexn", "Brexn", "Qrexg", "Brexg", "Qc", "Qalln", "Balln",
               "Gg", "Kg")
STRUCT_PROPS = ("q", "grain", "def", "phase")
PROCESS_PROPS = ("W", "H", "proj", "step", "samp", "term", "T")

def arrhenius(
        temperature: Union[float, np.ndarray],
        activation_energy: Union[float, np.ndarray],
        pre_exponential: Union[float, np.ndarray] = 1.0
    ) -> np.ndarray:
    """ Calculates an Arrhenius-form rate given T, E and A. If any of these is 
    a numpy vector, all other vectors should have the same shape. T should be
    in K. """
    return pre_exponential * np.exp(- activation_energy / 8.314 / temperature)


def probabilities(temperature: float) -> dict:
    """ Pull mat props into np array, apply Arrhenius formula vectorized, then 
    fill probabilities dict. """
    pass


# methods that act on fields
# -----------------------------------------------------------------------------
def enforce_boundary_condition(field: np.ndarray) -> np.ndarray:
    """ Enforces the periodic BC on field and returns a new field. """
    return np.pad(field, 1, 'wrap')


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
