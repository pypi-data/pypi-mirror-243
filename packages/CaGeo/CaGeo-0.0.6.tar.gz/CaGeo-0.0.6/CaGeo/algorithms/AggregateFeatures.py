import numpy as np
import scipy


def interpolate(val1, time1, val2, time2, time):
    interp = scipy.interpolate.interp1d([time1, time2], [val1, val2])

    return interp(time)


def rolling_window_test(a, window, window_type, time=None, distance=None):
    return _rolling_window(a, window, window_type, time, distance)


# window_type= None-> #features; 'time'-> time based; 'distance'-> distance based
def _rolling_window(a, window, window_type, time=None, distance=None):
    if window_type is None:
        shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
        strides = a.strides + (a.strides[-1],)
        for row in np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides):
            yield row
    elif window_type == 'time':  # TODO: optimize
        if time is None:
            raise ValueError(f"time cannot be None when window_type={window_type}")
        for i in range(len(time - 1)):
            total_time = 0
            values = []

            for j, (corr, succ) in enumerate(zip(time[i:-1], time[i + 1:])):
                delta = succ - corr
                if total_time + delta > window:
                    interpolated_value = interpolate(a[i + j], corr, a[i + j + 1], succ, window)
                    values.append(interpolated_value)
                    break
                else:
                    total_time += delta
                    values.append(a[i + j])
            yield values
    elif window_type == 'distance':  # TODO: optimize
        if distance is None:
            raise ValueError(f"distance cannot be None when window_type={window_type}")
        for i in range(len(distance - 1)):
            total_distance = 0
            values = []

            for j, corr, succ in enumerate(zip(distance[i:-1], distance[i + 1:])):
                delta = succ - corr
                if total_distance + delta > window:
                    interpolated_value = interpolate(a[i + j], corr, a[i + j + 1], succ, window)
                    values.append(interpolated_value)
                    break
                else:
                    total_distance += delta
                    values.append(a[i + j])
            yield values
    else:
        raise ValueError(f"window_type={window_type} unsupported. window_type must be in [None, 'time', 'distance']")


def _apply_np_fun(features: np.ndarray, window, window_type=None, time=None, distance=None, f=None):
    if window is None:
        window = len(features)

    if len(features) == 1:
        return features

    res = []

    for array in _rolling_window(features, window, window_type, time, distance):
        res.append(f(array))

    return np.array(res)

def sum(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.sum)


def max(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.max)


def min(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.min)

def mean(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.mean)


def std(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.std)


def cov(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.cov)


def var(features: np.ndarray, window, window_type=None, time=None, distance=None):
    return _apply_np_fun(features, window, window_type, time, distance, np.var)


def rate_upper(features: np.ndarray, threshold, window, distance=None, time=None, window_type=None):
    if window is None:
        window = len(features)

    returnValue = []

    for i, window_value in enumerate(_rolling_window(features, window, window_type, time, distance)):
        returnValue.append(0)
        for el in window_value:
            if el > threshold:
                returnValue[i] += 1

    returnValue = np.array(returnValue)

    if distance is not None:
        returnValue /= distance

    return returnValue


def rate_below(features: np.ndarray, threshold, window, distance=None, time=None, window_type=None):
    return rate_upper(features=features, threshold=threshold * -1, window=window, window_type=window_type,
                      distance=distance, time=time)
