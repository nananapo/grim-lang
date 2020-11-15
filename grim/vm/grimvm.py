from ..parser.interpreter import *
from ..error.vmerror import *
from .runstack import *

from ..formula.types import ClassType
from ..formula.primitive import *
from ..formula.variable import *

class GrimRunner:

    def __init__(self, parser):
        self.parser = parser

    #実行 (同時実行可能)
    def run(self):
        runstack = RunStack()
        runstack.run_function(self.parser.main, [])
        self.__run_fun(runstack)
        runstack.end_function()

    # Variable,Formulaを返す -> リストなら終了(return) リストの最初だけ使う
    def __run_fun(self, runstack):

        namespace, variables = runstack.get_process_and_variable()

        # 実行
        result = None
        for formula in namespace.process:

            result = self.__run_formula(formula, variables, runstack)

            #返り値がリスト => return
            if type(result) == list:
                if len(result) == 0:
                    return VariableNone()
                else:
                    return result[0]

        if result == None:
            result = VariableNone()

        #最後の結果を返す
        return result

    def __run_formula(self, parentformula, variables, runstack):

        assign_variable_name = parentformula.assign

        value = None
        search_assign = None  # 割り当て検索用

        #割り当てがある場合
        if assign_variable_name != None:

            #動的か静的か判別
            assign_dynamic = False
            if assign_variable_name[0] == ":":
                assign_variable_name = assign_variable_name[1::]
                assign_dynamic = True

            search_assign = runstack.searchVariable(
                assign_variable_name, dynamic=assign_dynamic)

            #割当先のvariableを探す
            if search_assign.result == SearchResult.RESULT_NOT_FOUND:
                value = VariableNone()
            elif search_assign.result == SearchResult.RESULT_VARIABLE:
                value = search_assign.variables[assign_variable_name]
            else:
                VariableNotFoundError(assign_variable_name).throw()

        #割り当て無し
        else:
            value = VariableNone()

        OP_EQUAL = 0
        op = OP_EQUAL

        for i in range(0, len(parentformula.value)):

            formula = parentformula.value[i]
            v_type = formula.get_type()

            #String演算
            if v_type == ClassType.TYPE_STRING:
                value = self.__calc(value, formula, op)

            #引数の明示された関数の実行
            elif v_type == ClassType.TYPE_RUNNABLE:

                # 引数を準備
                params = []
                for p in formula.parameters:
                    params.append(self.__run_formula(p, variables, runstack))

                # 実行する関数の名前
                runnable_name = formula.name

                #動的か静的か判別
                runnable_dynamic = False
                if runnable_name[0] == ":":
                    runnable_name = runnable_name[1::]
                    runnable_dynamic = True

                #検索
                search_runnable = runstack.searchVariable(
                    runnable_name, runnable_dynamic, function_only=True)

                #検索結果を処理
                #見つからない
                if search_runnable.result == SearchResult.RESULT_NOT_FOUND:
                    FunctionNotFoundError(runnable_name).throw()
                #ビルトイン関数だった
                elif search_runnable.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                    result = None
                    if runnable_name == "input":
                        if len(params) != 0:
                            print(*params)
                        result = String(input())
                    elif runnable_name == "print":
                        print(*params)
                        result = VariableNone()
                    elif runnable_name == "return":
                        return params
                    else:
                        #ビルトイン関数実装漏れ
                        FunctionNotFoundError(runnable_name).throw()

                    #計算
                    value = self.__calc(value, result, op)

                elif search_runnable.result == SearchResult.RESULT_FUNCTION:
                    #実行する
                    runnable_namespace = search_runnable.namespace.functions[runnable_name]
                    runstack.run_function(runnable_namespace, params)
                    result = self.__run_fun(runstack)
                    runstack.end_function()

                    # returnなら即終了
                    if type(result) == list:
                        return result

                    #計算
                    value = self.__calc(value, result, op)

            # 関数、または変数の計算
            elif v_type == ClassType.TYPE_VARIABLE:

                params = []

                # 実行する関数の名前
                runnable_name = formula.name

                #動的か静的か判別
                runnable_dynamic = False
                if runnable_name[0] == ":":
                    runnable_name = runnable_name[1::]
                    runnable_dynamic = True

                #検索
                search_runnable = runstack.searchVariable(
                    runnable_name, runnable_dynamic)

                #検索結果を処理
                #見つからない
                if search_runnable.result == SearchResult.RESULT_NOT_FOUND:
                    FunctionNotFoundError(runnable_name).throw()

                #ビルトイン関数だった
                elif search_runnable.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                    result = None
                    if runnable_name == "input":
                        if len(params) != 0:
                            print(*params)
                        result = String(input())
                    elif runnable_name == "print":
                        print(*params)
                        result = VariableNone()
                    elif runnable_name == "return":
                        return params
                    else:
                        #ビルトイン関数実装漏れ
                        FunctionNotFoundError(runnable_name).throw()

                    #計算
                    value = self.__calc(value, result, op)

                #関数だった
                elif search_runnable.result == SearchResult.RESULT_FUNCTION:

                    #実行する
                    runnable_namespace = search_runnable.namespace.functions[runnable_name]
                    runstack.run_function(runnable_namespace, params)
                    result = self.__run_fun(runstack)
                    runstack.end_function()

                    # returnなら即終了
                    if type(result) == list:
                        return result

                    #計算
                    value = self.__calc(value, result, op)

                #数字だった
                elif search_runnable.result == SearchResult.RESULT_NUMERIC:
                    #計算
                    value = self.__calc(value, search_runnable.numeric, op)

                #変数だった
                elif search_runnable.result == SearchResult.RESULT_VARIABLE:
                    value = self.__calc(
                        value, search_runnable.variables[runnable_name], op)

            #オペレーター変更
            elif v_type == ClassType.TYPE_OPERATOR:
                op = formula.get_op()

            else:
                print("Unknown Variable")

        if search_assign != None:
            # 変数に代入
            if search_assign.result == SearchResult.RESULT_NOT_FOUND:
                #新しく代入
                proc, variables = runstack.get_process_and_variable()
                variables[search_assign.name] = value
            elif search_assign.result == SearchResult.RESULT_VARIABLE:
                #代入
                search_assign.variables[search_assign.name] = value

        return value  # deepcopyの必要はない

    #計算する
    def __calc(self, value, entity, op):

        OP_EQUAL = 0
        OP_PLUS = 1
        OP_MINUS = 2
        OP_MUL = 3
        OP_DIV = 4

        if op == OP_EQUAL:
            return entity
        elif op == OP_PLUS:
            return value + entity
        elif op == OP_MINUS:
            return value - entity
        elif op == OP_MUL:
            return value * entity
        elif op == OP_DIV:
            return value / entity
