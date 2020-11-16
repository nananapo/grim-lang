
from .types import ClassType
from ..error.vmerror import UnknownOperationError

class Variable:
    def __init__(self, name):
        self.name = name
        self.value = None

    def get_type(self):
        return ClassType.TYPE_VARIABLE

    def __str__(self):
        return "Variable<"+self.name+">"


class VariableNone(Variable):

    def __init__(self):
        pass

    def get_type(self):
        return ClassType.TYPE_NONE

    def __str__(self):
        return "VariableNone"

    def __add__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC or o_type == ClassType.TYPE_STRING:
            return other + self
        elif o_type == ClassType.TYPE_NONE:
            return self
        else:
            UnknownOperationError(self, other, "+").throw()

    def __sub__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return other - self
        UnknownOperationError(self, other, "-").throw()

    def __mul__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return other * self
        elif o_type == ClassType.TYPE_NONE:
            return self
        else:
            UnknownOperationError(self, other, "*").throw()

    def __truediv__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return other / self
        elif o_type == ClassType.TYPE_NONE:
            return self
        UnknownOperationError(self, other, "/").throw()

class Runnable(Variable):  #
    def __init__(self, name, params=None):
        self.name = name
        self.parameters = params if params != None else []

    def __str__(self):
        return "Runnable<"+self.name+">" + str(self.parameters)

    def get_type(self):
        return ClassType.TYPE_RUNNABLE

class Indefinite: #計算はできない
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Indefinite<"+self.name+">"

    def get_type(self):
        return ClassType.TYPE_INDEFINITE
