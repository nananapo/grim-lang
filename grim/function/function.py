from ..error.parseerror import VariableNameError
from .builtin import BuiltIn

class Function:

    ROOT = 0

    TYPE_FUNCTION = -1  # 関数
    TYPE_OP_UNITE = 0  # オペレーター 左右二つを結合する , 引数二つ
    TYPE_OP_ALTER_RIGHT = 1  # オペレーター 右を変更する , 引数一つ uniteと被る名前もokにしたい

    def __init__(self, name, parent,function_type):
        self.name = name
        self.function_type = function_type
        self.process = [] # <Formula>のリスト
        self.parameters = [] #<Parameter>のリスト
        self.functions = {} # <Function>のリスト
        self.parent = parent

    def is_root(self):
        return self.parent == Function.ROOT

    def __str__(self):
        return ("Function" if self.function_type == Function.TYPE_FUNCTION else "Operator")+"<" + self.name+">"

    @staticmethod
    def check_function_name(name,parent,index):
        if name in BuiltIn.KEYWORD or ":" in name or ")" in name or name == ";" or '"' in name or "'" in name:
            VariableNameError(name, parent.name, index).throw()

class Parameter:

    def __init__(self,name):
        self.type_name = name[0] == ";"
        self.name = name[1::] if self.type_name else name

    @staticmethod
    def check_parameter_name(name, parent, index):
        if name in BuiltIn.KEYWORD or ":" in name or ")" in name or name == ";" or '"' in name or "'" in name:
            VariableNameError(name, parent.name, index).throw()
