from grim.parser.interpreter import *
from grim.error.vmerror import *
from grim.vm.runstack import *

from grim.formula.name import NameClass
from grim.formula.types import ClassType
from grim.formula.primitive import *
from grim.formula.variable import *

from grim.function.builtinrunner import BuiltInRunner


class GrimRunner:

    def __init__(self, parser,*,enable_debug = False):
        self.parser = parser
        self.enable_debug = enable_debug

    #実行 (同時実行可能)
    def run(self):
        runstack = RunStack()
        runstack.run_function(self.parser.main, {})
        self.__run_fun(runstack,-1)
        runstack.end_function()

    # デバッグ
    def debug(self,*msg,depth):
        if self.enable_debug:
            print("    "*depth , *msg)


    # Variable,Formulaを返す -> リストなら終了(return) リストの最初だけ使う
    # TODO 不定形は返せない 終了時の不定形を許さない
    # return_listは引数用 -> 結果を全て返す

    def __run_fun(self, runstack, depth,*,return_list=False, processes=None,run_func = False):

        depth += 1

        parentfunction, variables = runstack.get_process_and_variable()

        READ_FORB = 0
        READ_BORM = 1
        READ_FORB_MV = 2
        mode = READ_FORB

        formulas = []  # nowformula
        now_formula = [[], [], []]  # 単位 , op , 優先順位
        now_stack = [[], None, []]  # 一単位 => 先に値にする

        if processes == None:
            processes = parentfunction.process

        process_size = len(processes)

        self.debug("runfun", return_list, run_func, processes, depth=depth)

        index = 0

        while index < process_size:
            formula = processes[index]
            var = formula.value

            if isinstance(var,list):
                var = UncomputedFunction(var)

            var_type = var.get_type()

            self.debug("f", var_type, var, depth=depth)

            #
            if var_type == ClassType.TYPE_NONE or var_type == ClassType.TYPE_STRING or var_type == ClassType.TYPE_NUMERIC or var_type == ClassType.TYPE_INDEFINITE or var_type == ClassType.TYPE_NAME:
                pass
            #
            elif var_type == ClassType.TYPE_VARIABLE:

                # 検索
                search_result = runstack.search_variable(var.name)

                # 見つからない => その名前に不定形を割り当て TODO 名前許容
                if search_result.result == SearchResult.RESULT_NOT_FOUND:
                    variables[var.name] = Indefinite(var.name)
                    var = variables[var.name]
                # 変数
                elif search_result.result == SearchResult.RESULT_VARIABLE:
                    var = search_result.variables[var.name]
                # 引数なし関数
                elif search_result.result == SearchResult.RESULT_FUNCTION:

                    if run_func:
                        function = search_result.get_function()

                        # 引数の個数を確認
                        if len(function.parameters) != 0:
                            ParameterNotMatchError(function.name).throw()

                        # 実行する
                        runstack.run_function(function, {})
                        var = self.__run_fun(runstack,depth)
                        runstack.end_function()
                    else:
                        var = UncomputedFunction([formula])

                # 引数なしビルトイン関数
                elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                    if run_func:
                        var = BuiltInRunner.run_builtin(
                            search_result.name, [], runstack)

                        # return なら即終了
                        if isinstance(var, list):
                            if len(var) == 0:
                                return VariableNone()
                            else:
                                return var[0]
                    else:
                        var = UncomputedFunction([formula])

                # op
                elif search_result.result == SearchResult.RESULT_OPERATOR_FRONT or search_result.result == SearchResult.RESULT_OPERATOR_MID or search_result.result == SearchResult.RESULT_OPERATOR_BACK:
                    var = search_result.get_function()

                # 数値
                elif search_result.result == SearchResult.RESULT_NUMERIC:
                    var = search_result.numeric

            # 実行の場合
            elif var_type == ClassType.TYPE_RUNNABLE:

                # 検索
                search_result = runstack.search_variable(
                    var.name, function_only=True)

                # 見つからない => エラー
                if search_result.result == SearchResult.RESULT_NOT_FOUND:

                    FunctionNotFoundError(var.name).throw()

                # 引数あり関数 op1, op2も
                elif search_result.result == SearchResult.RESULT_FUNCTION or search_result.result == SearchResult.RESULT_OPERATOR_BACK or search_result.result == SearchResult.RESULT_OPERATOR_FRONT or search_result.result == SearchResult.RESULT_OPERATOR_MID:

                    if run_func:
                        function = search_result.get_function()

                        params_set = self.__run_fun(
                            runstack, depth=depth, return_list=True, processes=var.value)

                        # 実行する
                        runstack.run_function(
                            function, self.__assign_params(function, params_set))
                        var = self.__run_fun(runstack,depth)
                        runstack.end_function()
                    else:
                        var = UncomputedFunction([formula])

                # 引数ありビルトイン関数
                elif search_result.result == SearchResult.RESULT_BUILT_IN_FUNCTION:

                    if run_func:
                        params_set = self.__run_fun(
                            runstack, depth=depth, return_list=True, processes=var.value)

                        var = BuiltInRunner.run_builtin(
                            search_result.name, params_set, runstack)

                        # return なら即終了
                        if isinstance(var, list):
                            if len(var) == 0:
                                return VariableNone()
                            else:
                                return var[0]
                    else:
                        var = UncomputedFunction([formula])

            elif var_type == ClassType.TYPE_FORMULA:

                if run_func:
                    var = self.__run_fun(
                        runstack=runstack, depth=depth, processes=var.value)
                else:
                    var = UncomputedFunction(formula)
            
            elif var_type == ClassType.TYPE_UNCOMPOTED:

                if run_func:
                    var = self.__run_fun(depth=depth,
                        runstack=runstack, processes=var.process)
                else:
                    var = UncomputedFunction([formula])


            # 取得しなおし
            var_type = var.get_type()

            self.debug("b", var_type, var, depth=depth)

            # 最初の状態 front , variableのみ受付 variableでbormへ
            if mode == READ_FORB:

                # オペレーター
                if var_type == ClassType.TYPE_FUNCTION:

                    # b m は受け付けない
                    if var.function_type == Function.TYPE_OP_MID or var.function_type == Function.TYPE_OP_BACK:
                        VMError(reason="演算子の結合に失敗しました :State forb").throw()

                    now_stack[0].append(var)

                # 値
                else:
                    now_stack[1] = var
                    mode = READ_BORM

            # backかmidを受け付ける midでfvmvへ f,vで新しくforbへ
            elif mode == READ_BORM:

                # オペレーター
                if var_type == ClassType.TYPE_FUNCTION:

                    if var.function_type == Function.TYPE_OP_MID:

                        now_formula[0].append(now_stack)
                        now_formula[1].append(var)
                        now_formula[2].append(var.get_priority())
                        now_stack = [[], None, []]
                        mode = READ_FORB_MV

                    elif var.function_type == Function.TYPE_OP_BACK:

                        now_stack[2].append(var)

                    elif var.function_type == Function.TYPE_OP_FRONT:
                        now_formula[0].append(now_stack)
                        formulas.append(now_formula)
                        now_formula = [[], [], []]
                        now_stack = [[var], None, []]
                        mode = READ_FORB



                else:
                    now_formula[0].append(now_stack)
                    formulas.append(now_formula)
                    now_formula = [[], [], []]
                    now_stack = [[], var, []]
                    mode = READ_BORM

            # 前に式がある状態
            elif mode == READ_FORB_MV:

                # オペレーター
                if var_type == ClassType.TYPE_FUNCTION:

                    # b m は受け付けない
                    if var.function_type == Function.TYPE_OP_MID or var.function_type == Function.TYPE_OP_BACK:
                        VMError(reason="演算子の結合に失敗しました :State forb_mv").throw()

                    elif var.function_type == Function.TYPE_OP_FRONT:
                        now_stack[0].append(var)

                else:

                    now_stack[1] = var
                    mode = READ_BORM

            index += 1

        # 確認
        if mode == READ_FORB:
            if now_stack[1] == 0:
                VMError(reason="演算子の結合に失敗しました :State forb last").throw()
            else:
                now_formula[0].append(now_stack)
                formulas.append(now_formula)

        # 確認
        if mode == READ_BORM:
            now_formula[0].append(now_stack)
            formulas.append(now_formula)

        # 確認
        if mode == READ_FORB_MV:
            VMError(reason="演算子の結合に失敗しました :State forb_mv last").throw()

        # 確認
        if len(formulas[0]) == 0:
            formulas = [[VariableNone()], [], []]

        # 実行
        result_set = []
        for formula in formulas:
            self.debug("exec", formula, depth=depth)
            result_set.append(self.__run_formula(
                depth=depth, formulas=formula, runstack=runstack))


        # 結果を返す
        if return_list:
            self.debug("funend return_list", result_set, depth=depth)
            return result_set
        else:
            self.debug("funend result ", result_set[len(result_set)-1],depth=depth)
            return result_set[len(result_set)-1]

    # マイナス関係あり
    """
runfun False False [<grim.formula.formula.Formula object at 0x0000019461B974F0>]
f 1 Runnable<print>[<grim.formula.formula.Formula object at 0x0000019461B975E0>, <grim.formula.formula.Formula object at 0x0000019461B97670>]
b 7 <grim.function.function.UncomputedFunction object at 0x0000019461B97820>
exec [[[[], <grim.function.function.UncomputedFunction object at 0x0000019461B97820>, []]], [], []]
    formula start
        runfun False True [<grim.formula.formula.Formula object at 0x0000019461B974F0>]
        f 1 Runnable<print>[<grim.formula.formula.Formula object at 0x0000019461B975E0>, <grim.formula.formula.Formula object at 0x0000019461B97670>]
            runfun True False [<grim.formula.formula.Formula object at 0x0000019461B975E0>, <grim.formula.formula.Formula object at 0x0000019461B97670>]
            f 0 Variable<9>
            b 3 9
            f 0 Variable<°>
            b 6 Operator<°>
            exec [[[[], <grim.formula.primitive.Numeric object at 0x0000019461B978E0>, [<grim.function.function.Function object at 0x0000019461B970A0>]]], [], []]
                formula start
                全体 [[[[], <grim.formula.primitive.Numeric object at 0x0000019461B978E0>, [<grim.function.function.Function object at 0x0000019461B970A0>]]], [], []]
                formula end 9
            funend return_list [<grim.formula.primitive.Numeric object at 0x0000019461B978E0>]

        b -1 VariableNone
        exec [[[[], <grim.formula.variable.VariableNone object at 0x0000019461B979A0>, []]], [], []]
            formula start
            全体 [
                [
                    [
                        [],
                        <grim.formula.variable.VariableNone object at 0x0000019461B979A0>
                        , 
                        []
                    ]
                ], [], []
                ]
            formula end VariableNone
        funend result  VariableNone
    全体 [[[[], <grim.formula.variable.VariableNone object at 0x0000019461B979A0>, []]], [], []]
    formula end VariableNone
funend result  VariableNone

    """
    def __run_formula(self, *,depth,formulas,runstack):

        depth += 1

        #降順ソート
        formulas[2].sort(reverse = True)

        sizeO = len(formulas[2])

        self.debug("formula start", sizeO, depth=depth)

        if sizeO != 0:
            for i in range(0,sizeO):

                op = None
                opIndex = 0
                flop = None
                flopIndex = 0
                flleft = None

                for j in range(0,sizeO):
                    fun = formulas[1][j]

                    if fun.get_priority() == formulas[2][0]:
                        if flop == None:
                            op = fun
                            flop = fun
                            opIndex = j
                            flopIndex = j
                            flleft = fun.is_left_unite()
                        else:
                            if flleft != fun.is_left_unite():
                                op = flop
                                opIndex = flopIndex
                                break
                            else:
                                if not flleft:
                                    op = fun
                                    opIndex = j

                del formulas[2][0]

                pa1 = self.__run_op_bf(depth=depth,
                    formula=formulas[0][opIndex], runstack=runstack)
                pa2 = self.__run_op_bf(depth=depth,
                    formula=formulas[0][opIndex+1], runstack=runstack)

                self.debug("結合", pa1, pa2, op, depth=depth)

                runstack.run_function(op, self.__assign_params(op, [pa1,pa2]))
                var = self.__run_fun(runstack, depth,run_func=True)
                runstack.end_function()

                del formulas[1][opIndex]
                del formulas[0][opIndex+1]
                del formulas[0][opIndex]

                formulas[0].insert(opIndex,[[],var,[]])
                self.debug("結果", var, formulas, depth=depth)

                sizeO -= 1
            
        else:
            if formulas[0][0][1].get_type() == ClassType.TYPE_UNCOMPOTED:
                formulas[0][0][1] = self.__run_fun(runstack,depth,run_func=True,processes=formulas[0][0][1].process)

            formulas[0][0][1] = self.__run_op_bf(
                runstack=runstack, depth=depth, formula=formulas[0][0])

        self.debug("全体", formulas, depth=depth)
        self.debug("formula end", formulas[0][0][1], depth=depth)

        return formulas[0][0][1]



    # backとfrontのみをやる
    # 優先順位マイナスの考慮はopmidのみ
    # 同じなら左優先
    def __run_op_bf(self, *, depth,formula, runstack):

        depth += 1

        self.debug("runBF",depth=depth)

        sizeR = len(formula[0])
        sizeL = len(formula[2])
        sizeL_copy = sizeL
        var = formula[1]

        for i in range(0, sizeR+sizeL):

            if sizeR == 0:
                runstack.run_function(
                    formula[2][sizeL_copy-sizeL], self.__assign_params(formula[2][sizeL_copy-sizeL], [var]))
                var = self.__run_fun(runstack,  depth, run_func=True)
                runstack.end_function()
                sizeL -= 1
                continue
            elif sizeL == 0:
                runstack.run_function(
                    formula[0][sizeR-1], self.__assign_params(formula[0][sizeR-1], [var]))
                var = self.__run_fun(runstack,  depth, run_func=True)
                runstack.end_function()
                sizeL -= 1
                continue

            rfun = formula[0][sizeR-1]
            lfun = formula[2][sizeL_copy-sizeL]

            fun = None
            if rfun.get_priority() >= lfun.get_priority():
                fun = rfun
                sizeR -= 1
            else:
                fun = lfun
                sizeL -= 1

            runstack.run_function(fun, self.__assign_params(fun, [var]))
            var = self.__run_fun(runstack, depth,run_func=True)
            runstack.end_function()

        self.debug("endBF", var,depth=depth)

        return var

    #引数割り当て
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
