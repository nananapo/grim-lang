from ..error.vmerror import *
from ..function.builtin import BuiltIn
from ..formula.primitive import Numeric

#実行管理用
class RunStack:

    def __init__(self):
        self.namespace_set = []
        self.variable_set = []

    #関数を実行するときに呼ぶ
    def run_function(self, namespace, params):

        variables = {}

        #引数の個数を確認
        if len(namespace.parameters) != len(params):
            ParameterNotMatchError(namespace.name).throw()

        #引数を変数に割り当て
        i = 0
        for name in namespace.parameters:
            variables[name] == params[i]
            i += 1

        #追加
        self.variable_set.append(variables)
        self.namespace_set.append(namespace)

    #処理と変数を取得する
    def get_process_and_variable(self):
        index = len(self.namespace_set)-1
        return [self.namespace_set[index], self.variable_set[index]]

    #関数を終了したら呼ぶ
    def end_function(self):
        if len(self.variable_set) > 0:
            self.variable_set.pop()
            self.namespace_set.pop()

    #変数または関数を探して、SearchResultを返す
    def searchVariable(self, name, dynamic=False, function_only=False, variable_only=False):

        #動的束縛
        if dynamic:

            #戻って探していく
            for i in range(len(self.namespace_set)-1, -1, -1):
                #変数発見
                if not function_only and name in self.variable_set[i]:
                    return SearchResult(SearchResult.RESULT_VARIABLE, name, dynamic, variables=self.variable_set[i])
                #関数発見
                elif not variable_only and name in self.namespace_set[i].functions:
                    return SearchResult(SearchResult.RESULT_FUNCTION, name, dynamic, namespace=self.namespace_set[i])

        #静的束縛
        else:

            index = len(self.namespace_set) - 1
            namespace = self.namespace_set[index]
            parent = namespace

            while index >= 0:

                namespace = self.namespace_set[index]

                if namespace == parent:

                    variables = self.variable_set[index]
                    #変数発見
                    if not function_only and name in variables:
                        return SearchResult(SearchResult.RESULT_VARIABLE, name, dynamic, variables=variables)

                    #関数発見
                    elif not variable_only and name in namespace.functions:
                        return SearchResult(SearchResult.RESULT_FUNCTION, name, dynamic, namespace=namespace)

                    parent = namespace.parent

                index -= 1

        #ビルトイン関数
        if name in BuiltIn.BUILT_IN_FUNCS:
            return SearchResult(SearchResult.RESULT_BUILT_IN_FUNCTION, name, dynamic)

        #数字
        if not function_only:
            num = Numeric.is_num(name)
            if not isinstance(num, bool):
                return SearchResult(SearchResult.RESULT_NUMERIC, name, dynamic, numeric=num)

        #見つからない
        return SearchResult(SearchResult.RESULT_NOT_FOUND, name, dynamic)

#値検索の結果
class SearchResult:

    RESULT_NOT_FOUND = -1
    RESULT_VARIABLE = 0
    RESULT_FUNCTION = 1
    RESULT_BUILT_IN_FUNCTION = 2
    RESULT_NUMERIC = 3

    def __init__(self, result, name, dynamic, namespace=None, variables=None, numeric=None):
        self.result = result
        self.name = name
        self.dynamic = dynamic
        self.namespace = namespace
        self.variables = variables
        self.numeric = numeric
