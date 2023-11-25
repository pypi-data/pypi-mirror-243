"""Collection of numerical methods not found in standard libraries
"""

import numpy as np
from scipy.special import comb
from functools import cache

import maldives.utils as md


def robust_deriv(y, x, order=1, N=5, fill_value=None):
    """Low noise finite differentiator
    Suppresses high-frequency contribution to the numerical derivative.
    Requires tuning size of stencil in order to balance accuracy and smoothness.

    References:
        1. http://www.holoborodko.com/pavel/numerical-methods/numerical-derivative/smooth-low-noise-differentiators/

    Args:
        y (array): Function to take derivative on.
        x (array): Independent variable.
        order (int, optional): Order of derivative. Default is first-derivative.
        N (int, optional): Size of the stencil. Higher is more accurate but requires more data. Must be odd number. Default is 5.
        fill_value (float or None, optional): Value used to fill the derivative at boundaries. If None then calculate derivates by padding y with zeros.
    """
    if order not in [1, 2]:
        raise NotImplementedError(
            'Order must be 1 or 2. Higer-orders are not implemented.')
    if N % 2 != 1:
        raise ValueError('N must be an odd integer.')

    m = (N-3) // 2
    M = (N-1) // 2

    @cache
    def s(k):
        if k > M:
            return 0
        elif k == M:
            return 1
        return ((2*N-10)*s(k+1)-(N+2*k+3)*s(k+2))/(N-2*k-1)

    res = []

    NaNs = [np.nan] * (2*M)
    x_padded = np.concatenate((x.copy(), NaNs))
    y_padded = np.concatenate((y.copy(), NaNs))
    if fill_value is None:
        x_padded = md.fillna(x_padded)
        y_padded = md.fillna(y_padded)

    for i in range(len(y)):
        fp = 0
        for k in range(1, M+1):
            dx = (x_padded[i+k]-x_padded[i-k])/(2*k)
            if dx == 0:
                continue
            if order == 1:
                ck = (comb(2*m, m-k+1)-comb(2*m, m-k-1)) / 2**(N-2)
                fp += ck*(y_padded[i+k]-y_padded[i-k]) / dx
            elif order == 2:
                fp += (y_padded[i+k]-2*y_padded[i] +
                       y_padded[i-k])/dx**2*s(k) / 2**(N-3)
        res.append(fp)
    return (res if fill_value is None else md.fillna(res, fill_value))
