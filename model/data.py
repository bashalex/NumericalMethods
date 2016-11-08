import os

__p_path = "data/p_func.csv"
__s_path = "data/s_func.csv"
__z_path = "data/z_func.csv"
__coefs_path = "data/coefs.txt"
__cauchy_sol_path = "data/cauchy_solution.csv"

script_dir = os.path.dirname(__file__).replace('/model', '')


def __save_function(x, y, path):
    with open(os.path.join(script_dir, path), "w") as f:
        f.write(" ".join([str(item) for item in x]))
        f.write('\n')
        f.write(" ".join([str(item) for item in y]))
    print("function {} saved.".format(path))


def save_p_function(x, y):
    __save_function(x, y, __p_path)


def save_s_function(x, y):
    __save_function(x, y, __s_path)


def save_z_function(x, y):
    __save_function(x, y, __z_path)


def save_params(b, x0, y0, b1=None):
    with open(os.path.join(script_dir, __coefs_path), "w") as f:
        f.write(" ".join([b, x0, y0] if b1 is None else [b, x0, y0, b1]))
    print("params {}, {}, {} saved.".format(b, x0, y0))


def save_cauchy_solution(x, y, t):
    with open(os.path.join(script_dir, __cauchy_sol_path), "w") as f:
        f.write(" ".join([str(item) for item in x]))
        f.write('\n')
        f.write(" ".join([str(item) for item in y]))
        f.write('\n')
        f.write(" ".join([str(item) for item in t]))


def get_params():
    try:
        with open(os.path.join(script_dir, __coefs_path)) as f:
            return [float(e) for e in f.readline().split()]
    except FileNotFoundError:
        print("File {} Not Found!".format(__coefs_path))
        return None, None, None


def __get_function(path):
    try:
        with open(os.path.join(script_dir, path)) as f:
            x = [float(e) for e in f.readline().split()]
            y = [float(e) for e in f.readline().split()]
            return x, y
    except FileNotFoundError:
        print("File {} Not Found!".format(path))
        return None, None


def get_p_function():
    return __get_function(__p_path)


def get_s_function():
    return __get_function(__s_path)


def get_z_function():
    return __get_function(__z_path)
