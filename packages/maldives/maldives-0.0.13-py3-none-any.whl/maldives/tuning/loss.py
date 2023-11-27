import numpy as np


def total_variation(y, x):
    return abs(np.diff(y)/np.diff(x)).sum() * np.diff(x).mean()


def integral_rmse(dydx, y, x):
    """Calculate the RMSE between y estimated by integrating `dydx` and `y`

    Args:
        dydx (array): Estimated derivative of y
        y (array): Observed values of y
        x (array): Independent variable

    Raises:
        ValueError: x must be sorted

    Returns:
        RMSE (float): RMSE error between integral of `dydx` and `y`
    """
    if not np.all(np.diff(x) >= 0):
        raise ValueError('x is not sorted.')
    y_est = [y[0]]
    for i in range(1, len(x)):
        y_est.append(y[0]+np.trapz(dydx[:i+1], x[:i+1]))
    return np.sqrt(np.mean(np.subtract(y, y_est)**2))
