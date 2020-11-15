
from .types import ClassType

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

class Runnable(Variable):  #
    def __init__(self, name, params=None):
        self.name = name
        self.parameters = params if params != None else []

    def __str__(self):
        return "Runnable<"+self.name+">" + str(self.parameters)

    def get_type(self):
        return ClassType.TYPE_RUNNABLE
