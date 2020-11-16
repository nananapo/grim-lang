"""
いきなり-,op - はマイナス
全ては値渡し
"""
from grim.function.builtin import BuiltIn
from ..function.function import *
from ..formula.primitive import *
from ..formula.variable import *
from ..formula.formula import Formula
from ..error.vmerror import *
from grim.error.parseerror import *


class Parser:

    def __init__(self, string):
        self.program = string
        self.program_len = len(self.program)
        self.main = Function("main", Function.ROOT, Function.TYPE_FUNCTION)

    # read
    def read(self, i=0):
        self.__read_proc(i, self.main)

    # 区切りを判別
    def is_space(self, string):
        return string == " " or string == "\n"

    # funを読む
    """
    関数を定義するワード : fun,op1,op2
    
    #関数
    fun 関数名(引数1 引数2 ・・・)
        処理
    end
    引数が無い場合は括弧をスキップできる

    #op1,op2
    op1:引数を1つ持つオペレーター / 右の式に作用する
    op2:引数を2つ持つオペレーター / 左右の式に作用する
    """

    def __read_fun(self, i, parent, function):

        # 状態
        READ_ID = 0
        READ_PARAMS = 1
        READ_PARAMS_BRACKET = 2
        READ_PROC = 3
        mode = READ_ID

        # 設定
        strs = ""

        success = False

        while i < self.program_len:
            s = self.program[i]
            is_space = self.is_space(s)

            #print("rf", i, s, mode)

            # 関数名を読む
            if mode == READ_ID:

                if is_space:

                    # 名前被りはダメ
                    if strs in parent.functions:
                        FunctionAlreadyUsedError(strs, i).throw()

                    Function.check_function_name(strs, parent, i)  # 予約語チェック

                    function.name = strs
                    function.parent = parent

                    mode = READ_PARAMS_BRACKET
                    strs = ""

                elif s == "(":

                    # 名前被りはダメ
                    if strs in parent.functions:
                        FunctionAlreadyUsedError(strs, i).throw()

                    Function.check_function_name(strs, parent, i)  # 予約語チェック

                    function.name = strs
                    function.parent = parent

                    mode = READ_PARAMS
                    strs = ""

                else:
                    strs += s

            # 引数の最初の括弧を読む
            elif mode == READ_PARAMS_BRACKET:

                if is_space:
                    pass
                elif s == "(":
                    mode = READ_PARAMS
                # 引数スキップもできる
                else:
                    mode = READ_PROC
                    i -= 2

            # 引数を読む
            elif mode == READ_PARAMS:

                if is_space:

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in function.parameters:
                            ParameterNameError(strs, parent.name, i).throw()

                        Parameter.check_parameter_name(
                            strs, parent, i)  # 予約語チェック

                        # 追加
                        function.parameters.append(Parameter(strs))
                        strs = ""

                    else:
                        # 何もない場合はスキップ
                        pass

                elif s == ")":

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in function.parameters:
                            ParameterNameError(strs, parent.name, i).throw()

                        Parameter.check_parameter_name(
                            strs, parent, i)  # 予約語チェック

                        # 追加
                        function.parameters.append(Parameter(strs))
                        strs = ""

                    mode = READ_PROC

                else:
                    strs += s

            elif mode == READ_PROC:

                # 引数の個数チェック
                if function.function_type == Function.TYPE_OP_ALTER_RIGHT:
                    if len(function.parameters) != 1:
                        ParameterCountError(1, function.name)
                elif function.function_type == Function.TYPE_OP_UNITE:
                    if len(function.parameters) != 2:
                        ParameterCountError(2, function.name)

                i = self.__read_proc(i+1, function)
                success = True
                break

            i += 1

        if not success:
            EOFError(i).throw()

        return i-1

    # funを呼ぶときの引数を読む
    """
    全て式 スペース区切り
    ex
    式 式
    """

    def __read_fun_params(self, i, function, runnable):

        READ_BASE = 0
        READ_FORMULA = 1
        mode = READ_BASE

        formula_index = i
        bracket_size = 0  # (+1 )-1

        success = False

        while i < self.program_len:
            s = self.program[i]
            is_space = self.is_space(s)

            print("fp", i, s, mode,"b",bracket_size)

            success = False

            if mode == READ_BASE:

                if is_space:
                    pass
                elif s == "(":
                    bracket_size += 1
                elif s == ")":
                    if bracket_size == 0:
                        success = True
                        break
                    else:
                        bracket_size -= 1
                else:
                    formula_index = i
                    mode = READ_FORMULA

            elif mode == READ_FORMULA:
                if is_space:

                    if bracket_size == 0:
                    
                        formula = Formula()
                        fm_rs = self.__read_formula_value(
                            formula_index, function, formula, endIndex=i)
                        
                        if isinstance(fm_rs,int):
                            i = fm_rs
                            runnable.parameters.append(formula)
                            mode = READ_BASE

                elif s == "(":
                    bracket_size += 1
                elif s == ")":

                    if bracket_size == 0:

                        formula = Formula()
                        fm_rs = self.__read_formula_value(
                            formula_index, function, formula, endIndex=i)

                        if isinstance(fm_rs, int):
                            i = fm_rs
                            runnable.parameters.append(formula)
                            success = True
                        break

                    else:
                        bracket_size -= 1

                else:
                    pass
            i += 1

        if not success:
            EOFError(i).throw()

        return i+1

    # 式の値を読む
    """
    関数を呼ぶときは引数が無い場合スキップできる,引数アリのときの指定は(の前にスペースがあってはいけない
    endIndex はexclusive
    returnはi, return Falseは式が成立しなかった場合,return [i]は式でなかった場合(fun,op1,op2)
    """

    ID = 0

    def __read_formula_value(self, i, parent, formula, endIndex=None):

        myid = self.ID
        self.ID += 1
        print("formula called", myid)

        if endIndex == None:
            endIndex = self.program_len

        if i == endIndex:
            return False

        READ_VALUE = 0
        mode = READ_VALUE

        strs = ""

        success = False

        while i < endIndex:
            s = self.program[i]
            is_space = self.is_space(s)

            print("f", i, s, mode, parent.name)

            success = False

            if mode == READ_VALUE:
                if is_space:
                    if strs == "":
                        pass

                    elif strs in BuiltIn.KEYWORD:
                        if strs == "end":
                            ParseError(i).throw()

                        elif strs == "fun":

                            function = Function(
                                "undefined", parent, Function.TYPE_FUNCTION)
                            i = self.__read_fun(i+1, parent, function)
                            parent.functions[function.name] = function
                            strs = ""
                            success = True
                            return [i]

                        elif strs == "op1":

                            function = Function(
                                "undefined", parent, Function.TYPE_OP_ALTER_RIGHT)
                            i = self.__read_fun(i+1, parent, function)
                            parent.functions[function.name] = function
                            strs = ""
                            success = True
                            return [i]

                        elif strs == "op2":

                            function = Function(
                                "undefined", parent, Function.TYPE_OP_UNITE)
                            i = self.__read_fun(i+1, parent, function)
                            parent.functions[function.name] = function
                            strs = ""
                            success = True
                            return [i]

                    else:

                        # :だけはだめ
                        if strs == ":":
                            VariableNameError(strs, parent.name, i).throw()

                        formula.value = Variable(strs)
                        strs = ""
                        success = True
                        break

                # " => 文字
                elif s in String.SYMBOL:

                    # 文字を呼んで追加する
                    res = self.__read_str(i+1, s)
                    i, value = res[0], res[1]
                    
                    formula.value = value

                    strs = ""
                    success = True
                    break

                elif s == "(":

                    # 空なのにいきなり(がきたらエラー TODO 計算順序
                    if strs == "":
                        ParseError(i).throw()

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, parent.name, i).throw()

                    runnable = Runnable(strs)
                    i = self.__read_fun_params(i+1, parent, runnable)
                    formula.value = runnable

                    strs = ""
                    success = True
                    break
                else:
                    strs += s

            i += 1

        if not success:
            if mode == READ_VALUE:
                if strs != "":
                    formula.value = Variable(strs)
                else:
                    EOFError(i).throw()
            else:
                EOFError(i).throw()

        print(formula, myid)

        return i

    # 処理を読む
    """
    全ての処理は式
    一連の処理もオブジェクトに => ifとかも
    """

    def __read_proc(self, i, function):

        # 状態
        READ_BASE = 0
        READ_ASSIGN = 1
        mode = READ_BASE

        # 設定
        formula = None

        strs = ""
        assign_index = i

        success = False

        while i < self.program_len:
            s = self.program[i]
            is_space = self.is_space(s)

            print("p", i, s, mode)

            if mode == READ_BASE:

                if is_space:
                    pass

                # 文字開始
                elif s in String.SYMBOL:
                    
                    formula = Formula()
                    fm_rs = self.__read_formula_value(i, function, formula)

                    if isinstance(fm_rs,int):
                        i = fm_rs
                        function.process.append(formula)
                    elif isinstance(fm_rs, list):
                        i = fm_rs[0]

                # 変数名を読む
                else:
                    mode = READ_ASSIGN
                    strs = s
                    assign_index = i

            # 変数名を読む
            elif mode == READ_ASSIGN:

                if is_space:

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, function.name, i).throw()

                    if strs == "end":
                        success = True
                        break
                    
                    #式を追加
                    formula = Formula()
                    fm_rs = self.__read_formula_value(
                        assign_index, function, formula)

                    if isinstance(fm_rs, int):
                        i = fm_rs
                        function.process.append(formula)
                    elif isinstance(fm_rs, list):
                        i = fm_rs[0]

                    mode = READ_BASE
                    strs = ""

                # いきなり文字開始
                elif s in String.SYMBOL:

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, function.name, i).throw()

                    # 式を追加
                    formula = Formula()
                    fm_rs = self.__read_formula_value(
                        assign_index, function, formula)

                    if isinstance(fm_rs, int):
                        i = fm_rs
                        function.process.append(formula)
                    elif isinstance(fm_rs, list):
                        i = fm_rs[0]

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                # 引数ありRunnable
                elif s == "(":

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, function.name, i).throw()

                    if strs == "end":
                        print("不明なend")
                        ParseError(i).throw()

                    # 式を追加
                    formula = Formula()
                    fm_rs = self.__read_formula_value(
                        assign_index, function, formula)

                    if isinstance(fm_rs, int):
                        i = fm_rs
                        function.process.append(formula)
                    elif isinstance(fm_rs, list):
                        i = fm_rs[0]

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                else:
                    strs += s

            i += 1

        if not success:

            # endで終了の場合もある
            if strs == "end":
                pass
            elif strs != "":

                # 式を追加
                formula = Formula()
                fm_rs = self.__read_formula_value(
                    assign_index, function, formula)

                if isinstance(fm_rs,int):
                    i = fm_rs
                    function.process.append(formula)
                elif isinstance(fm_rs, list):
                    i = fm_rs[0]

            elif function == self.main:
                pass
            else:
                EOFError(i).throw()

        return i

    # 文字を読む
    """
    文字の定義
    "文字 \\ \n \" "
    TODO エスケープシーケンス
    """

    def __read_str(self, i, startWith):

        READ_STR = 0
        mode = READ_STR

        # 設定
        string = String()
        strs = ""

        success = False

        for i in range(i, len(self.program)):
            if mode == READ_STR:
                s = self.program[i]
                print("s", i, s)
                if s == startWith:
                    string.string = strs
                    success = True
                    break
                else:
                    strs += s

        if not success:
            EOFError(i).throw()

        return [i, string]
