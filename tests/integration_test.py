#! /usr/bin/python3.5
from model.integration import integrate_p_func
from model.tabulation import save_tabulated_func
from scipy.integrate import simps
from model import data

name = 'ρ(w)'

funcs = ['6w * (1 - w)']  # , '3w + sin(w)'

for i, func in enumerate(funcs):
    print('integrate {}...'.format(func))
    with open('function{}.txt'.format(i), 'w') as f:
        f.write('step, result, scipy result, diff\n')
    results = []
    for step in [0.00001, 0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006, 0.0007, 0.0008,
                 0.0009, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]:
        print("step = {}".format(step))
        # tabulate function and save to the file
        thread = save_tabulated_func(name, func, x0=0, x1=1, step=step)
        thread.join()
        print('tabulated')
        # load tabulated function
        x, y = data.get_p_function()
        print('loaded')
        # integrate it
        result = integrate_p_func(x, y, step=step)
        print('my result:', result)

        # integrate it using scipy
        scipy_result = simps(y, x)
        print('scipy result:', scipy_result)

        diff = abs(result - scipy_result)
        # count difference
        print("difference: {}".format(diff))
        with open('function{}.txt'.format(i), 'a') as f:
            f.write('{}, {}, {}, {}\n'.format(step, result, scipy_result, diff))
