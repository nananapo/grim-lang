# 実行時エラー
class VMError:
    def __init__(self, reason):
        self.error = "VMError : " + reason

    def name(self):
        return "VMError"

    def throw(self):
        print("実行中にエラーが発生しました : ", self.name())
        print(self.error)
        exit()


class FunctionNotFoundError(VMError):

    def __init__(self, fun):
        self.error = "関数 " + fun + "が見つかりませんでした"

    def name(self):
        return "FunctionNotFoundError"


class VariableNotFoundError(VMError):

    def __init__(self, var_id):
        self.error = "変数 " + var_id + "が見つかりませんでした"

    def name(self):
        return "VariableNotFoundError"


class ParameterIsNameClassError(VMError):

    def __init__(self, def_id, name):
        self.error = "関数 "+def_id+"の引数["+name+"]は名前型なので、名前型か不定型を渡す必要があります"

    def name(self):
        return "ParameterIsNameClassError"


class ParameterNotMatchError(VMError):

    def __init__(self, def_id):
        self.error = "関数 "+def_id+"の引数が一致しませんでした"

    def name(self):
        return "ParameterNotMatchError"


class UnknownOperationError(VMError):

    def __init__(self, target1, target2, operator):
        self.error = target1.__class__.__name__+"と" + \
            target2.__class__.__name__ + "の演算<"+operator+">が定義されていません(未定義動作)"

    def name(self):
        return "UnknownOperationError"


class ZeroDivisionError(VMError):

    def __init__(self):
        self.error = "0で割ることはできません"

    def name(self):
        return "ZeroDivisionError"


class NumericCastError(VMError):

    def __init__(self, string):
        self.error = "文字列 "+string+"は数値ではありません。"

    def name(self):
        return "NumericCastError"


class TypeError(VMError):

    def __init__(self, string):
        self.error = string

    def name(self):
        return "TypeError"
