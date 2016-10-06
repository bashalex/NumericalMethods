from model.integration import integrate_p_func
from model.interpolation import interpolate


def test1():
    print("Test integration of p function...")
    integral_vals = integrate_p_func()
    print("Test integration of p function...{}".format('OK' if sum(integral_vals) == 0 else 'ERROR'))
    print("Test interpolation...")
    interpolation = interpolate(integral_vals)
    print("Test interpolation...{}".format('OK' if sum(interpolation) == 3 else 'ERROR'))
    print("Test saving coefficients of interpolation to file...")
    with open('./data/interpolation_coefs.txt', 'w') as f:
        f.write(' '.join([str(e) for e in interpolation]))
    try:
        with open('./data/interpolation_coefs.txt', 'r') as f:
            print("Test saving coefficients of interpolation to file...{}"
                  .format('OK' if len(f.readline().split()) == 3 else 'ERROR'))
    except:
        print("Test saving coefficients of interpolation to file...ERROR")


def test2():
    pass


def run():
    test1()
    test2()
