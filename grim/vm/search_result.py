
# 値検索の結果
class SearchResult:

    RESULT_NOT_FOUND = -1
    RESULT_VARIABLE = 0
    RESULT_FUNCTION = 1
    RESULT_BUILT_IN_FUNCTION = 2
    RESULT_OPERATOR_FRONT = 3
    RESULT_OPERATOR_MID = 4
    RESULT_OPERATOR_BACK = 5
    RESULT_NUMERIC = 6

    def __init__(self, result, name, dynamic, function=None, variables=None, numeric=None):
        self.result = result
        self.name = name
        self.dynamic = dynamic
        self.function = function  # functionsが入る -> function.functions[name]
        self.variables = variables
        self.numeric = numeric

    def get_function(self):
        return self.function.functions[self.name]
