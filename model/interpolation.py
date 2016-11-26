from model import data
from model.linear_system_solver import solve


def __get_value(_x, m, x, y, step):
    if _x >= x[-1]:
        return x[-1]
    if _x <= x[0]:
        return x[0]

    i = int((_x - x[0]) // step)
    s1 = (y[i] * (x[i+1] - _x)**2 * (2 * (_x - x[i]) + step)) / step**3
    s2 = (y[i+1] * (_x - x[i])**2 * (2 * (x[i+1] - _x) + step)) / step**3
    s3 = (m[i] * (x[i+1] - _x)**2 * (_x - x[i])) / step**2
    s4 = (m[i+1] * (_x - x[i])**2 * (_x - x[i+1])) / step**2
    return s1 + s2 + s3 + s4


def interpolate(x, y):
    step = x[1] - x[0]
    N = len(x) - 1
    # build linear system:
    # m[i-1] + 4m[i] + m[i+1] = 3(y[i+1] - y[i-1]) / step for i = 1, 2, ..., N-1
    A = [[0. for i in range(len(x))] for j in range(len(x))]
    b = [0 if i == 0 or i == N else 3 * (y[i+1] - y[i-1]) / step for i in range(len(x))]
    for i in range(1, N):
        A[i][i-1] = 1
        A[i][i] = 4
        A[i][i+1] = 1
    m = solve(A, b)
    # approximate m[0] as y(0)'
    m[0] = (-11 * y[0] + 18 * y[1] - 9 * y[2] + 2 * y[3]) / (6 * step)
    # approximate m[N] as y(N)'
    m[N] = (11 * y[N] - 18 * y[N - 1] + 9 * y[N - 2] - 2 * y[N - 3]) / (6 * step)
    return lambda _x: __get_value(_x, m, x, y, step)

# x, y = data.get_p_function()
# f = interpolate(x, y)
# print(f(0.2))
