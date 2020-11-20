from grim.error.vmerror import UnknownOperationError
from grim.formula.types import ClassType


class Numeric:
    __NUMBER = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    def __init__(self, number):
        self.number = number

    def get_type(self):
        return ClassType.TYPE_NUMERIC

    def copy(self):
        return Numeric(self.number)

    # 文字列が数字か判定 -> False or 数値
    @staticmethod
    def is_num(string):

        if string == "+" or string == "-":
            return False

        front = False
        point = False
        for s in string:
            if not point:
                if s == "+" or s == "-":
                    if front:
                        return False
                    front = True
                elif s == ".":
                    point = True
                elif s in Numeric.__NUMBER:
                    pass
                else:
                    return False
            else:
                if s == "+" or s == "-":
                    return False
                elif s == ".":
                    return False
                elif s in Numeric.__NUMBER:
                    pass
                else:
                    return False
        return float(string) if point else int(string)

    def __str__(self):
        return str(self.number)

    def __add__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return Numeric(self.number+other.number)
        elif o_type == ClassType.TYPE_STRING:
            return String(str(self.number)+other.string)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "+").throw()

    def __sub__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return Numeric(self.number-other.number)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "-").throw()

    def __mul__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return Numeric(self.number*other.number)
        elif o_type == ClassType.TYPE_STRING:
            return String(self.number*other.string)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "*").throw()

    def __truediv__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            if other.number == 0:
                ZeroDivisionError().throw()
            return Numeric(self.number/other.number)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "/").throw()


class String:
    SYMBOL = ["\"", "'"]

    def __init__(self, string=""):
        self.string = string

    def get_type(self):
        return ClassType.TYPE_STRING

    def copy(self):
        return String(self.string)

    def __str__(self):
        return self.string  # "String<"+self.string+">"

    def __add__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return String(self.string+str(other.number))
        elif o_type == ClassType.TYPE_STRING:
            return String(self.string+other.string)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "+").throw()

    def __sub__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NONE:
            return self.copy()
        UnknownOperationError(self, other, "-").throw()

    def __mul__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NUMERIC:
            return Numeric(self.string*other.number)
        elif o_type == ClassType.TYPE_NONE:
            return self.copy()
        else:
            UnknownOperationError(self, other, "*").throw()

    def __truediv__(self, other):
        o_type = other.get_type()
        if o_type == ClassType.TYPE_NONE:
            return self.copy()
        UnknownOperationError(self, other, "/").throw()


class Boolean:

    def __init__(self, value):
        self.value = value

    def get_type(self):
        return ClassType.TYPE_BOOLEAN

    def __str__(self):
        return "True" if self.value else "False"
