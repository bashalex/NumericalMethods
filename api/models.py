
class Step:
    def __init__(self, _id, name):
        self.id = _id
        self.name = name


class Params:
    def __init__(self, b, x, y):
        self.b = b
        self.x = x
        self.y = y

steps = [Step(1, "Load Distribution"),
         Step(2, "Load Plan"),
         Step(3, "Choose function"),
         Step(4, "Load traffic"),
         Step(5, "Results")]

params = Params(0.01, 0, 0)
