# From: Indices of movement behaviour: conceptual background, effects of scale and location errors
import math
from scipy.stats import variation

import numpy as np

import CaGeo.algorithms.BasicFeatures as bf


def straightness(lat: np.ndarray, lon: np.ndarray, accurate=False):
    dE = bf.distance(np.array([lat[0], lat[-1]]), np.array([lon[0], lon[-1]]), accurate=accurate)
    L = bf.distance(lat, lon, accurate=accurate).sum()

    return (dE / L)[1]


def meanSquaredDisplacement(lat: np.ndarray, lon: np.ndarray):
    return lat.var() + lon.var()


def intensityUse(lat: np.ndarray, lon: np.ndarray, accurate=False):
    L = bf.distance(lat, lon, accurate=accurate).sum()
    A = (np.max(lat) - np.min(lat)) * (np.max(lon) - np.min(lon))

    if A == .0:
        return np.NAN

    if accurate:
        raise RuntimeWarning("Accurate area estimation is not implemented")

    return L / math.sqrt(A)


def sinuosity(lat: np.ndarray, lon: np.ndarray, accurate=False):
    p = bf.distance(lat, lon, accurate=accurate).mean()  # mean step length
    c = np.cos(bf.turningAngles(lat, lon)).mean()
    s = np.sin(bf.turningAngles(lat, lon)).mean()
    b = variation(bf.distance(lat, lon, accurate=accurate))

    return 2 * ((p * ((1 - c ** 2 - s ** 2) / ((1 - c) ** 2 + s ** 2) + b ** 2)) ** -.5)
