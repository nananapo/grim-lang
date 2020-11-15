class ParseError:
    def __init__(self, index=0):
        index = str(index)
        self.error = "ParseError :インデックス " + index

    def name(self):
        return "ParseError"

    def throw(self):
        print("構文解析中にエラーが発生しました : ", self.name())
        print(self.error)
        exit()


class ParameterNameError(ParseError):

    def __init__(self, param, def_id, index):
        index = str(index)
        self.error = "引数名 " + param + " は既に使用されています :関数名 " + def_id + " :インデックス " + index

    def name(self):
        return "ParameterNameError"


class FunctionAlreadyUsedError(ParseError):

    def __init__(self, def_id, index):
        index = str(index)
        self.error = "関数名 " + def_id + " は既に使用されています :インデックス "+index

    def name(self):
        return "FunctionAlreadyUsedError"


class EOFError(ParseError):

    def __init__(self, index):
        index = str(index)
        self.error = "構文解析中にファイルが終了しました :インデックス "+index

    def name(self):
        return "EOFError"


class VariableNameError(ParseError):

    def __init__(self, variable, def_id, index):
        index = str(index)
        self.error = "変数名 " + variable + \
            " は予約語として既に使用されています :関数名 " + def_id + " :インデックス " + index

    def name(self):
        return "VariableNameError"
