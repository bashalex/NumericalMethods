import sympy
import numpy as np
from threading import Thread
from model import data
from settings import p_func_tabulations_step


class Save(Thread):
    def __init__(self, name, function, p_step, x0, x1, callback=None):
        Thread.__init__(self, daemon=True)
        self.name = name
        self.function = function
        self.callback = callback
        self.p_step = p_step
        self.x0 = x0
        self.x1 = x1

    def run(self):
        if self.name == 'ρ(w)':
            x, y = self.tabulate(self.function, self.x0, self.x1, self.p_step)
            data.save_p_function(x, y)
        if self.name == 'S(t)':
            x, y = self.tabulate(self.function, 0, 100, 1)
            data.save_s_function(x, y)
        if self.name == 'z(t)':
            x, y = self.tabulate(self.function, 0, 100, 1)
            data.save_z_function(x, y)
        if self.callback is not None:
            self.callback()

    def tabulate(self, function, start, end, step):
        w, t = sympy.symbols('w t')
        x, y = [], []
        if type(function) is str:
            expr = self.parse(function)
            for i in np.arange(start, end + (step / 2), step):
                x.append(i)
                y.append(expr.evalf(subs={w: i, t: i}))
        else:
            for i in np.arange(start, end + (step / 2), step):
                x.append(i)
                y.append(function(i))
        return x, y

    def parse(self, function):
        # insert * between numbers and variables if necessary
        i = 0
        while i < len(function):
            symb = function[i]
            if i > 0 and (not (symb.isdigit() or symb in {' ', '*', '(', ')', '^', '+', '-', '/', '.'})) and\
                    function[i-1].isdigit():
                function = function[:i] + "*" + function[i:]
            i += 1
        return sympy.sympify(function)


def save_tabulated_func(name, function, step=p_func_tabulations_step, x0=0, x1=1, callback=None):
    thread = Save(name, function, step, x0, x1, callback)
    thread.start()
    return thread
