import numpy as np


def solve(f0, f1, t, x0, y0):
    """
    :param f0: f(t, x, y) - python function
    :param f1: f(t, x, y) - python function
    :param t: list of floats
    :param x0: x(t0) = x0
    :param y0: y(t0) = y0
    :return: tabulated x and y that are solution for the following system:
    x' = f0(t, x, y)
    y' = f1(t, x, y)
    """
    x, y = np.zeros(len(t)), np.zeros(len(t))
    x[0], y[0] = x0, y0

    for i in range(len(t) - 1):
        # calculate step
        step = t[i+1] - t[i]
        # calculate coefficients
        kx1 = f0(t[i], x[i], y[i]) * step
        ky1 = f1(t[i], x[i], y[i]) * step
        kx2 = f0(t[i] + step / 2., x[i] + kx1 / 2., y[i] + ky1 / 2.) * step
        ky2 = f1(t[i] + step / 2., x[i] + kx1 / 2., y[i] + ky1 / 2.) * step
        kx3 = f0(t[i] + step / 2., x[i] + kx2 / 2., y[i] + ky2 / 2.) * step
        ky3 = f1(t[i] + step / 2., x[i] + kx2 / 2., y[i] + ky2 / 2.) * step
        kx4 = f0(t[i] + step, x[i] + kx3, y[i] + ky3) * step
        ky4 = f1(t[i] + step, x[i] + kx3, y[i] + ky3) * step
        # calculate current values
        x[i+1] = x[i] + (kx1 + 2 * kx2 + 2 * kx3 + kx4) / 6.
        y[i+1] = y[i] + (ky1 + 2 * ky2 + 2 * ky3 + ky4) / 6.
    return x, y
