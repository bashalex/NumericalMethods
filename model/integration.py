from settings import p_func_tabulations_step


def integrate_p_func(x, y, step=p_func_tabulations_step):
    return __integrate(x, y, step)


def __integrate(x, y, step):
    # Simpson's rule
    N = len(y)  # number of points
    print("num of steps:", N-1)
    if N % 2 != 0:
        return (step / 3.) * sum([y[k-1] + 4 * y[k] + y[k+1] for k in range(1, N - 1, 2)])
    else:
        res1 = (step / 3.) * sum([y[k-1] + 4 * y[k] + y[k+1] for k in range(1, N - 2, 2)]) +\
               (y[N-1] + y[N-2]) * (step / 2.)
        res2 = (step / 3.) * sum([y[k-1] + 4 * y[k] + y[k+1] for k in range(2, N - 1, 2)]) +\
               (y[0] + y[1]) * (step / 2.)
        return (res1 + res2) / 2.
