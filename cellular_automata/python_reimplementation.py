# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 23:41:05 2019

@author: tothp
"""
import numpy as np

from scipy import signal
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
# these are the category and property names
CATS = {"Material": {"Tall", "Qallg", "Ballg", "Estor"},
        "PHASE0": {"Qrexn", "Brexn", "Qrexg", "Brexg", "Qc", "Qalln", "Balln",
               "Gg", "Kg"},
        "PHASE1": {"Qrexn", "Brexn", "Qrexg", "Brexg", "Qc", "Qalln", "Balln",
               "Gg", "Kg"},
        "Process": {"W", "H", "proj", "step", "samp", "term", "T"},
        "Structure": {"q", "grain", "def", "phase"}}

def _clear_string(string: str) -> str:
    return string.strip().replace("[", "").replace("]", "")


def _parse_line(line: str) -> Tuple:
    return _clear_string(line).split("\t")


def _check_constants(constants: dict) -> None:
    for category in CATS:
        if category not in constants:
            raise ValueError(
                    "Category {} not found in constants.".format(category))
        for prop in CATS[category]:
            if prop not in constants[category]:
                raise ValueError(
                        "Property {} not found in category {}.".format(
                                prop, category))


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
            constants[category].update({prop: float(value)})
        else:
            raise ValueError("Invalid parsed line {}".format(parsed))
    _check_constants(constants)
    return constants


# methods related to updating probabilities
# -----------------------------------------------------------------------------
# these are the order of property names for vectorized Arrhenius rate calc
MAT_ORDER = ("Estor", "Qallg", "Ballg")
PHASE_ORDER = ("Qrexn", "Qrexg", "Qc", "Brexn", "Brexg", "Qalln", "Balln")
PROB_PROPS = ("Se", "Ag", "Abg", "Rn", "Rg", "Co", "Rbn", "Rgb", "An", "Abn")

def arrhenius(
        temperature: Union[float, np.ndarray],
        activation_energy: Union[float, np.ndarray],
        pre_exponential: Union[float, np.ndarray] = 1.0
    ) -> np.ndarray:
    """ Calculates an Arrhenius-form rate given T, E and A. If any of these is 
    a numpy vector, all other vectors should have the same shape. T should be
    in K. """
    return pre_exponential * np.exp(- activation_energy / 8.314 / temperature)


class Probabilities:

    def __init__(self, constants: dict) -> None:
        self._constants = None
        self.values = None
        self._init_constants(constants)

    def __call__(self, temperature: float) -> dict:
        return self.calculate(temperature)

    def _init_constants(self, constants) -> None:
        _constants = []
        for prop in MAT_ORDER:
            _constants.append(constants["Material"][prop])
        for prop in PHASE_ORDER:
            _constants.append(constants["PHASE0"][prop])
        for prop in PHASE_ORDER:
            _constants.append(constants["PHASE1"][prop])
        self._constants = np.array(_constants)

    def calculate(self, temperature: float) -> None:
        self.values = arrhenius(temperature, self._constants)
        probabilities = {}
        for k, prop in enumerate(PROB_PROPS):
            if k < 3:
                probabilities[prop] = self.values[k]
            else:
                probabilities[prop] = [self.values[k], self.values[k + 7]]
        return probabilities


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
