#実行時エラー
class VMError:
    def __init__(self):
        self.error = "VMError"

    def name(self):
        return "VMError"

    def throw(self):
        print("実行中にエラーが発生しました : ", self.name())
        print(self.error)
        exit()


class FunctionNotFoundError(VMError):

    def __init__(self, def_id):
        self.error = "関数 " + def_id + "が見つかりませんでした"

    def name(self):
        return "FunctionNotFoundError"


class VariableNotFoundError(VMError):

    def __init__(self, var_id):
        self.error = "変数 " + var_id + "が見つかりませんでした"

    def name(self):
        return "VariableNotFoundError"


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
        self.error = "0で割ることはできません(未定義動作)"

    def name(self):
        return "ZeroDivisionError"
