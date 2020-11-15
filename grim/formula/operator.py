from .types import ClassType

class Operator:

    SYMBOL = ["+", "-", "*", "/", "%"]

    SYMBOL_DICT = {
        "+": 1,
        "-": 2,
        "*": 3,
        "/": 4
    }

    def __init__(self, op):
        self.operator = op

    def get_type(self):
        return ClassType.TYPE_OPERATOR

    def get_op(self):
        return Operator.SYMBOL_DICT[self.operator]

    def __str__(self):
        return "Operator<"+self.operator + ">"
