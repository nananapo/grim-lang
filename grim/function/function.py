from grim.formula.primitive import String
from grim.formula.types import ClassType
from grim.function.builtin import BuiltIn


class Function:

    # 開始キーワード
    SYMBOL = [
        "fun",
        "opf",
        "opm",
        "opb",
        "end"
    ]

    ROOT = 0  # 親

    TYPE_FUNCTION = -1  # 関数
    TYPE_OP_MID = 0  # 中置演算子
    TYPE_OP_FRONT = 1  # 前置演算子
    TYPE_OP_BACK = 2  # 後置演算子

    def __init__(self, *, name, parent, function_type, priority=0):
        self.name = name
        self.parent = parent
        self.function_type = function_type
        self.priority = priority
        self.process = []  # <Formula>のリスト
        self.parameters = []  # <Parameter>のリスト
        self.functions = {}  # <Function>のリスト

    def is_root(self):
        return self.parent == Function.ROOT

    def get_priority(self):
        return abs(self.priority)

    # 正なら左から結合する
    def is_left_unite(self):
        return self.priority > 0

    def __str__(self):
        return ("Function" if self.function_type == Function.TYPE_FUNCTION else "Operator")+"<" + self.name+">"

    @staticmethod
    def check_name(name):
        return not (name in BuiltIn.MARK or name in Function.SYMBOL or name in String.SYMBOL or name)

    @staticmethod
    def symbol2type(symbol):
        return {
            "fun": Function.TYPE_FUNCTION,
            "opf": Function.TYPE_OP_FRONT,
            "opm": Function.TYPE_OP_MID,
            "opb": Function.TYPE_OP_BACK
        }[symbol]

    # functiontypeではない
    def get_type(self):
        return ClassType.TYPE_FUNCTION


class Parameter:

    def __init__(self, name):
        self.type_name = name[0] == ";"
        self.name = name[1::] if self.type_name else name

    @staticmethod
    def check_name(name):
        return not (name in BuiltIn.MARK or name in Function.SYMBOL or name in String.SYMBOL)


class UncomputedFunction:

    def __init__(self, process):
        self.process = process

    # functiontypeではない
    def get_type(self):
        return ClassType.TYPE_UNCOMPUTED
