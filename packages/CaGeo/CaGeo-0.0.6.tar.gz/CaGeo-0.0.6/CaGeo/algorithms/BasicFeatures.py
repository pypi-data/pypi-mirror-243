import numpy as np
import geopy.distance as gp

def speed(lat: np.ndarray, lon: np.ndarray, time: np.ndarray, accurate=False):
    d_time = time[1:] - time[:-1]
    if type(accurate) is bool:
        dist = distance(lat, lon, accurate=accurate)[1:]
    else:
        dist = accurate

    return np.append([.0], dist / d_time)


def acceleration(lat: np.ndarray, lon: np.ndarray, time: np.ndarray, accurate=False):
    d_time = time[1:] - time[:-1]
    if type(accurate) is bool:
        dist = distance(lat, lon, accurate=accurate)[1:]
    else:
        dist = accurate

    return np.append([.0], dist / (d_time ** 2))


def acceleration2(lat: np.ndarray, lon: np.ndarray, time: np.ndarray, accurate=False):
    d_time = time[1:] - time[:-1]
    if type(accurate) is bool:
        dist = distance(lat, lon, accurate=accurate)[1:]
    else:
        dist = accurate

    acc = np.append([.0], dist / (d_time ** 2))

    return np.append([.0], acc[1:] - acc[:-1])


def direction(lat: np.ndarray, lon: np.ndarray):
    dist_lat = lat[1:] - lat[:-1]
    dist_lon = lon[1:] - lon[:-1]

    return np.append([.0], np.arctan2(dist_lat, dist_lon))

def turningAngles(lat: np.ndarray, lon: np.ndarray):
    direct = direction(lat, lon)

    return np.append([.0], direct[1:]-direct[:-1])


def distance(lat: np.ndarray, lon: np.ndarray, ellipsoid="WGS-84", accurate=True):
    if accurate:
        returnValue = np.zeros(len(lat) - 1)
        for i in range(len(lat) - 1):
            returnValue[i] = gp.geodesic((lat[i], lon[i]), (lat[i + 1], lon[i + 1]), ellipsoid=ellipsoid).km

        return np.append([.0], returnValue)

    else:
        dist_lat = lat[1:] - lat[:-1]
        dist_lon = lon[1:] - lon[:-1]
        dist = (dist_lat ** 2 + dist_lon ** 2) ** .5
        return np.append([.0], dist)*111.139
