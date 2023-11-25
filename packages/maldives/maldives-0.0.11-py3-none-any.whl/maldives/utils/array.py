# %%
import numpy as np

def shift(x, n, fill_value=None):
    """Shift 1D array by n elements

    Args:
        x (array): 1D array to be shifted
        n (int): Number of places to be shifted. Negative shifts element to the left.
        fill (float or None): Value used to fill the empty space created. If None then use the closest value. Default is None.
    """
    if n == 0:
        return x
    res = np.roll(x, n)
    if n > 0:
        res[:n] = res[n] if fill_value is None else fill_value
    elif n < 0:
        res[n:] = res[n-1] if fill_value is None else fill_value
    return res

def fillna(x, fill_value=0):
    x = np.asarray(x)
    x[np.isnan(x)] = fill_value
    return x