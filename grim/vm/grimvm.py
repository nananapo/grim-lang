from ..parser.interpreter import *
from ..error.vmerror import *
from .runstack import *

from ..formula.name import NameClass
from ..formula.types import ClassType
from ..formula.primitive import *
from ..formula.variable import *

from ..function.builtinrunner import BuiltInRunner


class GrimRunner:

    def __init__(self, parser):
        self.parser = parser

    #実行 (同時実行可能)
    def run(self):
        runstack = RunStack()
        runstack.run_function(self.parser.main, {})
        self.__run_fun(runstack)
        runstack.end_function()

    # Variable,Formulaを返す -> リストなら終了(return) リストの最初だけ使う
    # TODO 不定形は返せない
    # return_listは引数用 -> 結果を全て返す
    def __run_fun(self, runstack, return_list=False, processes=None):

        parentfunction, variables = runstack.get_process_and_variable()

        # 実行
        index = 0
        result = None
        result_set = []

        # TODO 計算順序を付けるなら list にして処理を別に回す必要がある
        # TODO 複数回のop1の対応
        last_variable = None
        last_operator_1 = None
        last_operator_2 = None

        READ_OP1_OR_VARIABLE = 0
        READ_MUST_OPERATOR = 1
        READ_MUST_VARIABLE = 2
        mode = READ_OP1_OR_VARIABLE

        if processes == None:
            processes = parentfunction.process

        while index < len(processes):
            formula = processes[index]
            variable = formula.value
            variable_type = variable.get_type()

            # 最初の状態
            if mode == READ_OP1_OR_VARIABLE:

                # 文字
                if variable_type == ClassType.TYPE_STRING:

                    last_variable = variable
                    mode = READ_MUST_OPERATOR

                # 数字
                elif variable_type == ClassType.TYPE_NUMERIC:

                    last_variable = variable
                    mode = READ_MUST_OPERATOR

                # 変数 mustop (数値文字は↑同様), 関数,builtin mustop , op2 error , op1 mustvar , num mustop , 見つからない 不定型を追加
                elif variable_type == ClassType.TYPE_VARIABLE:

                    # 検索
                    search_result = runstack.search_variable(variable.name)

                    # 見つからない => その名前に不定形を割り当て
                    if search_result.result == SearchResult.RESULT_NOT_FOUND:

                        variables[variable.name] = Indefinite(variable.name)
                        last_variable = variables[variable.name]
                        mode = READ_MUST_OPERATOR

                    # 変数
                    elif search_result.result == SearchResult.RESULT_VARIABLE:

                        last_variable = search_result.variables[variable.name]
                        mode = READ_MUST_OPERATOR

                    # 引数なし関数
                    elif search_result.result == SearchResult.RESULT_FUNCTION:

                        function = search_result.get_function()

                        # 引数の個数を確認
                        if len(function.parameters) != 0:
                            ParameterNotMatchError(function.name).throw()

                        # 実行する
                        runstack.run_function(function, {})
                        last_variable = self.__run_fun(runstack)
                        runstack.end_function()

                        mode = READ_MUST_OPERATOR

                    # 引数なしビルトイン関数
                    elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                        result = BuiltInRunner.run_builtin(
                            search_result.name, [], runstack)

                        # return なら即終了
                        if isinstance(result, list):
                            if len(result) == 0:
                                return VariableNone()
                            else:
                                return result[0]

                        last_variable = result
                        mode = READ_MUST_OPERATOR

                    # op1
                    elif search_result.result == SearchResult.RESULT_OPERATOR_ALTER_RIGHT:

                        last_operator_1 = search_result.get_function()
                        mode = READ_MUST_VARIABLE

                    # op2 無だったらエラー
                    elif search_result.result == SearchResult.RESULT_OPERATOR_UNITE:
                        
                        if last_variable == None:
                            VMError().throw()
                        else:
                            last_operator_2 = search_result.get_function()
                            mode = READ_MUST_VARIABLE

                    # 数値
                    elif search_result.result == SearchResult.RESULT_NUMERIC:

                        last_variable = search_result.numeric
                        mode = READ_MUST_OPERATOR

                # 実行の場合
                elif variable_type == ClassType.TYPE_RUNNABLE:

                    # 検索
                    search_result = runstack.search_variable(
                        variable.name, function_only=True)

                    # 見つからない => エラー
                    if search_result.result == SearchResult.RESULT_NOT_FOUND:

                        FunctionNotFoundError(variable.name).throw()

                    # 引数あり関数
                    elif search_result.result == SearchResult.RESULT_FUNCTION:

                        function = search_result.get_function()

                        params_set = self.__run_fun(
                            runstack, return_list=True, processes=variable.parameters)

                        # 実行する
                        runstack.run_function(
                            function, self.__assign_params(function, params_set))
                        last_variable = self.__run_fun(runstack)
                        runstack.end_function()

                        mode = READ_MUST_OPERATOR

                    # 引数ありビルトイン関数
                    elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                        params_set = self.__run_fun(
                            runstack, return_list=True, processes=variable.parameters)

                        result = BuiltInRunner.run_builtin(
                            search_result.name, params_set, runstack)

                        # return なら即終了
                        if isinstance(result, list):
                            if len(result) == 0:
                                return VariableNone()
                            else:
                                return result[0]

                        last_variable = result
                        mode = READ_MUST_OPERATOR

                    # op1
                    elif search_result.result == SearchResult.RESULT_OPERATOR_ALTER_RIGHT:

                        last_operator_1 = search_result.get_function()
                        mode = READ_MUST_VARIABLE

                    # op2 -> エラー
                    elif search_result.result == SearchResult.RESULT_OPERATOR_UNITE:

                        VMError().throw()

                else:
                    VMError().throw()

            # 前に式がある状態
            elif mode == READ_MUST_OPERATOR:

                # 文字
                if variable_type == ClassType.TYPE_STRING or variable_type == ClassType.TYPE_NUMERIC:

                    if return_list == True:
                        result_set.append(last_variable)
                    last_variable = None
                    mode = READ_OP1_OR_VARIABLE
                    continue

                #
                elif variable_type == ClassType.TYPE_VARIABLE:

                    # 検索
                    search_result = runstack.search_variable(variable.name)

                    # op2
                    if search_result.result == SearchResult.RESULT_OPERATOR_UNITE:

                        last_operator_2 = search_result.get_function()
                        mode = READ_MUST_VARIABLE

                    # その他
                    else:

                        if return_list == True:
                            result_set.append(last_variable)
                        last_variable = None
                        mode = READ_OP1_OR_VARIABLE
                        continue

                # 実行の場合
                elif variable_type == ClassType.TYPE_RUNNABLE:

                    if return_list == True:
                        result_set.append(last_variable)
                    last_variable = None
                    mode = READ_OP1_OR_VARIABLE
                    continue

                else:
                    VMError().throw()

            # 前にop1かop2がある状態
            elif mode == READ_MUST_VARIABLE:

                # 文字
                if variable_type == ClassType.TYPE_STRING or variable_type == ClassType.TYPE_NUMERIC:

                    # op1
                    if last_operator_1 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_1, self.__assign_params(last_operator_1, [variable]))
                        variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_1 = None

                    # op 2
                    if last_operator_2 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_2, self.__assign_params(last_operator_2, [last_variable, variable]))
                        last_variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_2 = None

                    mode = READ_OP1_OR_VARIABLE

                #
                elif variable_type == ClassType.TYPE_VARIABLE:

                    # 検索
                    search_result = runstack.search_variable(variable.name)

                    # 見つからない => その名前に不定型を割り当て
                    if search_result.result == SearchResult.RESULT_NOT_FOUND:

                        variable = Indefinite(variable.name)
                        variables[variable.name] = variable

                    # 変数
                    elif search_result.result == SearchResult.RESULT_VARIABLE:

                        variable = search_result.variables[variable.name]

                    # 引数なし関数
                    elif search_result.result == SearchResult.RESULT_FUNCTION:

                        function = search_result.get_function()

                        # 引数の個数を確認
                        if len(function.parameters) != 0:
                            ParameterNotMatchError(function.name).throw()

                        # 実行する
                        runstack.run_function(function, {})
                        variable = self.__run_fun(runstack)
                        runstack.end_function()

                    # 引数なしビルトイン関数
                    elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                        result = BuiltInRunner.run_builtin(
                            search_result.name, [], runstack)

                        # return なら即終了
                        if isinstance(result, list):
                            if len(result) == 0:
                                return VariableNone()
                            else:
                                return result[0]

                        variable = result

                    # op2
                    elif search_result.result == SearchResult.RESULT_OPERATOR_UNITE:

                        VMError().throw()# TODO 詳細表示

                    #op1
                    elif search_result.result == SearchResult.RESULT_OPERATOR_ALTER_RIGHT:
                        
                        #TODO 複数対応
                        if last_operator_1 == None:
                            last_operator_1 = search_result.get_function()
                            index += 1
                            continue
                        else:
                            VMError().throw()  # TODO 詳細表示        

                    # 数値
                    elif search_result.result == SearchResult.RESULT_NUMERIC:

                        variable = search_result.numeric

                    # op1
                    if last_operator_1 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_1, self.__assign_params(last_operator_1, [variable]))
                        variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_1 = None

                    # op 2
                    if last_operator_2 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_2, self.__assign_params(last_operator_2, [last_variable, variable]))
                        last_variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_2 = None

                    mode = READ_OP1_OR_VARIABLE

                # 実行の場合
                elif variable_type == ClassType.TYPE_RUNNABLE:

                    # 検索
                    search_result = runstack.search_variable(variable.name)

                    # op1,op2,見つからない -> エラー
                    if search_result.result == SearchResult.RESULT_NOT_FOUND or search_result.result == SearchResult.RESULT_OPERATOR_ALTER_RIGHT or search_result.result == SearchResult.RESULT_OPERATOR_UNITE:

                        VMError().throw()

                    # 変数
                    elif search_result.result == SearchResult.RESULT_VARIABLE:

                        variable = search_result.variables[variable.name]

                    # 引数あり関数
                    elif search_result.result == SearchResult.RESULT_FUNCTION:

                        function = search_result.get_function()

                        params_set = self.__run_fun(
                            runstack, return_list=True, processes=variable.parameters)

                        # 実行する
                        runstack.run_function(
                            function, self.__assign_params(function, params_set))
                        variable = self.__run_fun(runstack)
                        runstack.end_function()

                    # 引数ありビルトイン関数
                    elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                        params_set = self.__run_fun(
                            runstack, return_list=True, processes=variable.parameters)
                        result = BuiltInRunner.run_builtin(
                            search_result.name, params_set, runstack)

                        # return なら即終了
                        if isinstance(result, list):
                            if len(result) == 0:
                                return VariableNone()
                            else:
                                return result[0]

                        variable = result

                    # 数値
                    elif search_result.result == SearchResult.RESULT_NUMERIC:

                        variable = search_result.numeric

                    # op1
                    if last_operator_1 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_1, self.__assign_params(last_operator_1, [variable]))
                        variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_1 = None

                    # op 2
                    if last_operator_2 != None:

                        # 実行する
                        runstack.run_function(
                            last_operator_2, self.__assign_params(last_operator_2, [last_variable, variable]))
                        last_variable = self.__run_fun(runstack)
                        runstack.end_function()

                        #リセット
                        last_operator_2 = None

                    mode = READ_OP1_OR_VARIABLE

            index += 1

        if mode == READ_MUST_VARIABLE:
            VMError().throw()

        if last_variable != None:
            result_set.append(last_variable)

        if return_list:
            #結果セットを返す
            return result_set
        else:
            # 最後の結果を返す
            return last_variable

    def __assign_params(self, function, params_set):

        # 引数を変数に割り当て
        params = {}
        i = 0

        # 引数の個数を確認
        if len(function.parameters) != len(params_set):
            ParameterNotMatchError(function.name).throw()

        for parameter in function.parameters:

            # 受け取り手が名前型
            if parameter.type_name:
                par_type = params_set[i].get_type()
                if par_type == ClassType.TYPE_INDEFINITE:
                    params[parameter.name] = NameClass(
                        params_set[i].name)
                elif par_type == ClassType.TYPE_NAME:
                    params[parameter.name] = params_set[i]
                elif par_type == ClassType.TYPE_STRING:
                    params[parameter.name] = NameClass(
                        params_set[i].string)
                else:
                    ParameterIsNameClassError(
                        function.name, parameter.name).throw()
                i += 1
                continue
            
            params[parameter.name] = params_set[i]
            i += 1

        return params
