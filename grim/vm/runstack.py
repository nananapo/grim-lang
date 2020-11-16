from ..error.vmerror import *
from ..function.builtin import BuiltIn
from ..formula.primitive import Numeric
from ..function.function import Function

#実行管理用
class RunStack:

    def __init__(self):
        self.function_set = []
        self.variable_set = []

    # 関数を実行するときに呼ぶ
    def run_function(self, function, params):

        variables = params

        #追加
        self.variable_set.append(variables)
        self.function_set.append(function)

    #処理と変数を取得する
    def get_process_and_variable(self):
        index = len(self.function_set)-1
        return [self.function_set[index], self.variable_set[index]]

    #関数を終了したら呼ぶ
    def end_function(self):
        if len(self.variable_set) > 0:
            self.variable_set.pop()
            self.function_set.pop()

    #変数または関数を探して、SearchResultを返す
    def search_variable(self, name,function_only=False, variable_only=False):

        #動的か静的か判別
        dynamic = False
        if name[0] == ":":
            name = name[1::]
            dynamic = True

        #動的束縛
        if dynamic:

            #戻って探していく
            for i in range(len(self.function_set)-1, -1, -1):

                function = self.function_set[i]

                #変数発見
                if not function_only and name in self.variable_set[i]:
                    return SearchResult(SearchResult.RESULT_VARIABLE, name, dynamic, variables=self.variable_set[i])
                #関数発見
                elif not variable_only and name in self.function_set[i].functions:
                    fun_type = function.functions[name].function_type

                    if fun_type == Function.TYPE_FUNCTION:
                        return SearchResult(SearchResult.RESULT_FUNCTION, name, dynamic, function=function)
                    elif fun_type == Function.TYPE_OP_ALTER_RIGHT:
                        return SearchResult(SearchResult.RESULT_OPERATOR_ALTER_RIGHT, name, dynamic, function=function)
                    elif fun_type == Function.TYPE_OP_UNITE:
                        return SearchResult(SearchResult.RESULT_OPERATOR_UNITE, name, dynamic, function=function)

        #静的束縛
        else:

            index = len(self.function_set) - 1
            function = self.function_set[index]
            parent = function

            while index >= 0:

                function = self.function_set[index]

                if function == parent:

                    variables = self.variable_set[index]
                    #変数発見
                    if not function_only and name in variables:
                        return SearchResult(SearchResult.RESULT_VARIABLE, name, dynamic, variables=variables)

                    #関数発見
                    elif not variable_only and name in function.functions:
                        fun_type = function.functions[name].function_type

                        if fun_type == Function.TYPE_FUNCTION:
                            return SearchResult(SearchResult.RESULT_FUNCTION, name, dynamic, function=function)
                        elif fun_type == Function.TYPE_OP_ALTER_RIGHT:
                            return SearchResult(SearchResult.RESULT_OPERATOR_ALTER_RIGHT, name, dynamic, function=function)
                        elif fun_type == Function.TYPE_OP_UNITE:
                            return SearchResult(SearchResult.RESULT_OPERATOR_UNITE, name, dynamic, function=function)

                    parent = function.parent

                index -= 1

        #ビルトイン関数
        if name in BuiltIn.BUILT_IN_FUNCS:
            return SearchResult(SearchResult.RESULT_BUILT_IN_FUNCTION, name, dynamic)

        #数字
        if not function_only:
            num = Numeric.is_num(name)
            if not isinstance(num, bool):
                return SearchResult(SearchResult.RESULT_NUMERIC, name, dynamic, numeric=Numeric(num))

        #見つからない
        return SearchResult(SearchResult.RESULT_NOT_FOUND, name, dynamic)

#値検索の結果
class SearchResult:

    RESULT_NOT_FOUND = -1
    RESULT_VARIABLE = 0
    RESULT_FUNCTION = 1
    RESULT_BUILT_IN_FUNCTION = 2
    RESULT_OPERATOR_ALTER_RIGHT = 3
    RESULT_OPERATOR_UNITE = 4
    RESULT_NUMERIC = 5

    def __init__(self, result, name, dynamic, function=None, variables=None, numeric=None):
        self.result = result
        self.name = name
        self.dynamic = dynamic
        self.function = function # functionsが入る -> function.functions[name]
        self.variables = variables
        self.numeric = numeric

    def get_function(self):
        return self.function.functions[self.name]