from functools import reduce


def _LUdecomposition(A):
    L = [[0.] * len(A) for i in range(len(A))]
    U = [[0.] * len(A) for i in range(len(A))]

    P = _pivot_matrix(A)
    M = _multiply(P, A)

    # decomposition:
    for j in range(len(A)):
        L[j][j] = 1.

        for i in range(j + 1):
            U[i][j] = M[i][j] - sum(U[k][j] * L[i][k] for k in range(i))

        for i in range(j, len(A)):
            if U[j][j] == 0:
                U[j][j] = 1e-32
            L[i][j] = (M[i][j] - sum(U[k][j] * L[i][k] for k in range(j))) / U[j][j]

    return P, L, U


def _multiply(A, B):
    return [[sum(a * b for a, b in zip(row_m, col_n)) for col_n in zip(*B)] for row_m in A]


def _pivot_matrix(A):
    # generate E matrix
    pivot = [[float(i == j) for i in range(len(A))] for j in range(len(A))]

    for j in range(len(A)):
        row = max(range(j, len(A)), key=lambda i: abs(A[i][j]))
        if j != row:
            pivot[j], pivot[row] = pivot[row], pivot[j]

    return pivot


def _solve(L, U, b):
    # forward substitution
    y = b[:]
    for i in range(len(b)):
        for j in range(i):
            y[i] -= L[i][j] * y[j]
        if L[i][i] == 0:
            L[i][i] = 1e-32
        y[i] /= L[i][i]

    # backward substitution
    x = y[:]
    for i in range(len(b) - 1, -1, -1):
        for j in range(i + 1, len(b)):
            x[i] -= U[i][j] * x[j]
        if U[i][i] == 0:
            U[i][i] = 1e-32
        x[i] /= U[i][i]
    return x


def solve(A, b):
    # we solve linear system Ax = b where A = LU
    # Therefore LUx = b.Then let's say y = Ux
    # => we have a system to solve:
    # Ly = b
    # Ux = y
    # Here we go:

    # decompose matrix A
    P, L, U = _LUdecomposition(A)

    # we changed some rows therefore we must change elements in b as well
    b1 = b[:]
    for i in range(len(P)):
        for j in range(len(P)):
            if P[i][j] == 1:
                b1[i] = b[j]
    return _solve(L, U, b1)


def det(A):
    # calculate determinant of matrix A using LU-decomposition
    P, L, U = _LUdecomposition(A)
    sign = 1 if (len(P) - sum([P[i][i] for i in range(len(P))])) % 4 == 0 else -1
    return reduce(lambda x, y: x * y, [L[i][i] * U[i][i] for i in range(len(U))]) * sign


def inverse(A):
    P, L, U = _LUdecomposition(A)
    result = [[] for i in range(len(A))]
    for i in range(len(A)):
        for j, elem in enumerate(_solve(L, U, [(1 if j == i else 0) for j in range(len(A))])):
            result[j].append(elem)
    return result


def max_abs_sum_norm(A):
    return max(sum(map(abs, A[i])) for i in range(len(A)))
