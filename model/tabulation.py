import sympy
import numpy as np
from threading import Thread
from model import data


class Save(Thread):
    def __init__(self, name, function):
        Thread.__init__(self, daemon=True)
        self.name = name
        self.function = function

    def run(self):
        if self.name == 'ρ(w)':
            x, y = self.tabulate(self.function, 0, 1, 0.01)
            data.save_p_function(x, y)
        if self.name == 'S(t)':
            x, y = self.tabulate(self.function, 0, 100, 1)
            data.save_s_function(x, y)
        if self.name == 'z(t)':
            x, y = self.tabulate(self.function, 0, 100, 1)
            data.save_z_function(x, y)

    def tabulate(self, function, start, end, step):
        w, t = sympy.symbols('w t')
        expr = self.parse(function)
        x, y = [], []
        for i in np.arange(start, end, step):
            x.append(i)
            y.append(expr.evalf(subs={w: i, t: i}))
        return x, y

    def parse(self, function):
        # insert * between numbers and variables if necessary
        i = 0
        while i < len(function):
            symb = function[i]
            if i > 0 and (not (symb.isdigit() or symb in {' ', '*', '(', ')', '^', '+', '-', '/'})) and\
                    function[i-1].isdigit():
                function = function[:i] + "*" + function[i:]
            i += 1
        return sympy.sympify(function)


def save_func(name, function):
    thread = Save(name, function)
    thread.start()
    return thread
