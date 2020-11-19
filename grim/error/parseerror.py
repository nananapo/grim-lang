class ParseError:
    def __init__(self, index, *, reason):
        index = str(index)
        self.error = "ParseError :理由 "+reason+" :インデックス " + index

    def name(self):
        return "ParseError"

    def throw(self):
        print("構文解析中にエラーが発生しました : ", self.name())
        print(self.error)
        exit()


class ParameterNameError(ParseError):

    def __init__(self, index, *, param, fun):
        index = str(index)
        self.error = "引数名 " + param + " は既に使用されています :関数名 " + fun + " :インデックス " + index

    def name(self):
        return "ParameterNameError"


class ParameterCountError(ParseError):

    def __init__(self, *, need, fun):
        need = str(need)
        self.error = "オペレーターの引数は" + need + "個である必要があります :オペレーター名" + fun

    def name(self):
        return "ParameterCountError"


class FunctionAlreadyUsedError(ParseError):

    def __init__(self, index, *, name):
        index = str(index)
        self.error = "関数名 " + name + " は既に使用されています :インデックス "+index

    def name(self):
        return "FunctionAlreadyUsedError"


class EOFError(ParseError):

    def __init__(self, index, *, info):
        index = str(index)
        self.error = "構文解析中にファイルが終了しました :情報 "+info+" :インデックス "+index

    def name(self):
        return "EOFError"


class VariableNameError(ParseError):

    def __init__(self, index, *, variable):
        index = str(index)
        self.error = "変数名 " + variable + \
            " は予約語として既に使用されている、または使用不可能な文字が含まれています :インデックス " + index

    def name(self):
        return "VariableNameError"


class VariableKeywordError(ParseError):

    def __init__(self, index, *, variable):
        index = str(index)
        self.error = variable + "は予約語として既に使用されています :インデックス " + index

    def name(self):
        return "VariableKeywordError"
