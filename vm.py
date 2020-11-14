from interpreter import *

class GrimVM:

    BUILT_IN_FUNCS = set([
        "input",
        "print",
        "return"
    ])

    def __init__(self, parser):
        self.parser = parser

    def run(self):
        self.__run_fun("main", [])

    # Variable,Formulaを返す -> リストなら終了(return) リストの最初だけ使う
    def __run_fun(self, fun_id, params):

        # 関数が見つからない
        if not fun_id in self.parser.functions:
            if fun_id in GrimVM.BUILT_IN_FUNCS:
                if fun_id == "input":
                    if len(params) != 0:
                        print(*params)
                    res = input()
                    return String(res)
                elif fun_id == "print":
                    print(*params)
                    return VariableNone()
                elif fun_id == "return":
                    return params
            else:
                number = Numeric.is_num(fun_id)
                if isinstance(number, bool):
                    FunctionNotFoundError(fun_id).throw()
                else:
                    return Numeric(number)

        fun = self.parser.functions[fun_id]

        # 引数が合わない
        if len(params) != len(fun[0]):
            ParameterNotMatchError(fun_id).throw()

        # 変数用意
        variables = {}
        index = 0
        for param in fun[0]:
            variables[param] = params[index]
            index += 1

        # 実行
        result = VariableNone()
        for formula in fun[1]:
            result = self.__run_formula(formula, variables)
            #返り値がリスト => return
            if type(result) == list:
                if len(result) == 0:
                    return VariableNone()
                else:
                    return result[0]
        
        #最後の結果を返す
        return result

    def __run_formula(self, parentformula, variables):

        assign = parentformula.assign

        OP_EQUAL = 0
        op = OP_EQUAL

        value = None
        if assign != None and assign in variables:
            value = variables[assign]
        else:
            value = VariableNone()

        for i in range(0, len(parentformula.value)):

            formula = parentformula.value[i]
            v_type = formula.get_type()

            if v_type == Variable.TYPE_STRING:
                value = self.__calc(value, formula, op)

            elif v_type == Variable.TYPE_RUNNABLE:

                # 引数を準備
                params = []
                for p in formula.parameters:
                    params.append(self.__run_formula(p, variables))

                # 実行
                result = self.__run_fun(formula.name, params)

                # returnなら即終了
                if type(result) == list:
                    return result

                value = self.__calc(
                    value, result, op)

            elif v_type == Variable.TYPE_OPERATOR:
                op = formula.get_op()

            elif v_type == Variable.TYPE_VARIABLE:
                if formula.name in variables:
                    value = self.__calc(value, variables[formula.name], op)
                else:
                    result = self.__run_fun(formula.name, [])

                    # returnなら即終了
                    if type(result) == list:
                        return result

                    value = self.__calc(
                        value, result, op)

            else:
                print("Unknown Variable")

        # 変数に代入
        if assign != None:
            variables[assign] = value

        return value  # コピーではないのでdeepcopyしないといけない => 必要ないかも? => 全ての式はVariableNoneへの代入からなっているから必要が無い

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


class ParameterNotMatchError(VMError):

    def __init__(self, def_id):
        self.error = "関数 "+def_id+"の引数が一致しませんでした"

    def name(self):
        return "ParameterNotMatchError"


class UnknownOperationError(VMError):

    def __init__(self, target1, target2, operator):
        self.error = target1.__class__.__name__+"と"+target2.__class__.__name__ + "の演算<"+operator+">が定義されていません(未定義動作)"

    def name(self):
        return "UnknownOperationError"

class ZeroDivisionError(VMError):

    def __init__(self):
        self.error = "0で割ることはできません(未定義動作)"

    def name(self):
        return "ZeroDivisionError"
