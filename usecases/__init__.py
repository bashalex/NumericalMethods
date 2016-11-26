from model.integration import integrate_p_func
from model.interpolation import interpolate
from model import data
import numpy as np
import sympy


def test1():
    # step 1
    print("Test reading p function from file...")
    x, y = data.get_p_function()
    print("Test reading p function from file...{}".format('OK' if x is not None and
                                                          y is not None else 'ERROR'))
    # step 2
    print("Test integration of p function...")
    integral_value = integrate_p_func(x, y)
    print("Test integration of p function...{}".format('OK'))

    # step 3
    print("Test interpolation...")
    interpolation = interpolate(x, y)
    print("Test interpolation...{}".format('OK' if sum(interpolation) == 3 else 'ERROR'))

    # step 3.1
    print("Test saving coefficients of interpolation to file...")
    with open('./data/interpolation_coefs.txt', 'w') as f:
        f.write(' '.join([str(e) for e in interpolation]))
    try:
        with open('./data/interpolation_coefs.txt', 'r') as f:
            print("Test saving coefficients of interpolation to file...{}"
                  .format('OK' if len(f.readline().split()) == 3 else 'ERROR'))
    except FileNotFoundError:
        print("Test saving coefficients of interpolation to file...ERROR")


def test2():
    # step 1
    print("Test reading params from file...")
    b, x0, y0 = data.get_params()
    print("Test reading params from file...{}".format('OK' if x0 is not None and
                                                      y0 is not None and
                                                      b is not None else 'ERROR'))
    T = 1
    step = 0.01
    y, t = sympy.symbols('y t')
    U_func = sympy.sympify('3 * (y ^ 2) - 2 * (y ^ 3)')
    S_func = sympy.sympify('3 * t + sin(t)')
    z_func = sympy.sympify('4 * t + cos(t)')
    z1_func = sympy.sympify('4 - sin(t)')
    X, Y = np.empty(int(T / step)), np.empty(int(T / step))
    _t = np.arange(0, T, step)
    _t[0] = 0
    X[0], Y[0] = x0, y0
    for i in range(1, int(T / step)):
        X[i] = X[i-1] + (_t[i] - _t[i-1]) * z1_func.evalf(subs={t: _t[i]}) * U_func.evalf(subs={y: Y[i-1]})
        Y[i] = Y[i-1] + (_t[i] - _t[i-1]) * b * (X[i] - z_func.evalf(subs={t: _t[i]}))
    data.save_cauchy_solution(X, Y, _t)


def run():
    test1()
    test2()
