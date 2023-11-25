"""Collection of smoothing methods not found in standard libraries
"""

import numpy as np

def anisotropic_smoothing1d(y0, dx, steps, K, dt=1e-6, diffusion_type='cauchy'):
    """1D anisotropic diffusion smoothing
    References:
        1. https://www.cs.sfu.ca/~stella/papers/blairthesis/main/node25.html
        2. https://en.wikipedia.org/wiki/Anisotropic_diffusion

    Args:
        y0 (array): Function to be smoothed.
        dx (float or array): Grid size.
        steps (int): Number of integration steps. More steps results more smoothing.
        K (float): Width of the diffusion kernel
        dt (float, optional): Time step. Must be small for convergence. Defaults to 1e-6.
        diffusion_type (str, optional):Type of diffusion kernel. Defaults to 'cauchy'.

    Returns:
        yt (array): Smoothed function.
    """
    fcauchy = lambda x: 1/(1+(x/K)**2)
    fgauss = lambda x: np.exp(-(x/K)**2)
    f = fgauss if diffusion_type == 'gauss' else fcauchy

    yt = y0.copy()
    for _ in range(steps):
        fdiff = np.diff(yt,append=yt[0]) # forward difference
        bdiff = np.diff(yt[::-1],append=yt[-1])[::-1] # backward difference
        flow_right = fdiff*f(abs(fdiff)/dx) / dx**2
        flow_left =  bdiff*f(abs(bdiff)/dx) / dx**2
        yt += dt*(flow_right+flow_left + (y0-yt))
    return yt