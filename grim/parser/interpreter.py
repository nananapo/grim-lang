from grim.function.function import *
from grim.formula.primitive import *
from grim.formula.variable import *
from grim.formula.formula import Formula
from grim.error.vmerror import *
from grim.error.parseerror import *


class Parser:

    def __init__(self, file, debug=False):

        # ファイル読み込み
        lines = file.readlines()

        string = ""
        for line in lines:
            string += line

        # 解析
        self.program = string
        self.program_len = len(self.program)
        self.enable_debug = debug
        self.main = Function(name="main", parent=Function.ROOT,
                             function_type=Function.TYPE_FUNCTION)

    # read
    def read(self):
        self.__read_process(index=0, function=self.main)

    # 区切りを判別
    def is_space(self, string):
        return string == " " or string == "\n"

    # デバッグ
    def debug(self, *msg):
        if self.enable_debug:
            print(*msg)

    # funを読む
    def __read_fun(self, *, index, parent, function_type):

        # 状態
        READ_ID = 0
        READ_PRIORITY = 1
        READ_PARAMS = 2
        READ_PROC = 3

        if function_type == Function.TYPE_FUNCTION:
            mode = READ_ID
        else:
            mode = READ_PRIORITY

        # 設定
        strs = ""
        success = False
        function = Function(parent=parent, name=None,
                            function_type=function_type)

        while index < self.program_len:
            s = self.program[index]
            is_space = self.is_space(s)

            self.debug("rf", index, s, mode)

            # 関数名を読む
            if mode == READ_ID:

                if is_space:

                    # 予約語チェック
                    if not Function.check_name(strs):
                        FunctionAlreadyUsedError(index, name=strs)

                    function.name = strs
                    function.parent = parent

                    mode = READ_PROC
                    strs = ""

                elif s == "(":

                    # 予約語チェック
                    if not Function.check_name(strs):
                        FunctionAlreadyUsedError(index, name=strs)

                    function.name = strs
                    function.parent = parent

                    mode = READ_PARAMS
                    strs = ""

                else:
                    strs += s

            elif mode == READ_PRIORITY:

                if is_space:

                    if strs != "":
                        res = Numeric.is_num(strs)
                        if isinstance(res, bool):
                            ParseError(
                                index, reason="オペレーターの優先度は数値である必要があります").throw()
                        else:
                            function.priority = res

                        mode = READ_ID
                        strs = ""

                else:
                    strs += s

            # 引数を読む
            elif mode == READ_PARAMS:

                if is_space:

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in function.parameters:
                            ParameterNameError(
                                index, param=strs, fun=function.name).throw()

                        # 予約語チェック
                        if not Parameter.check_name(strs):
                            VariableNameError(index, variable=strs)

                        # 追加
                        function.parameters.append(Parameter(strs))
                        strs = ""

                elif s == ")":

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in function.parameters:
                            ParameterNameError(
                                index, param=strs, fun=function.name).throw()

                        # 予約語チェック
                        if not Parameter.check_name(strs):
                            VariableNameError(index, variable=strs)

                        # 追加
                        function.parameters.append(Parameter(strs))
                        strs = ""

                    mode = READ_PROC

                else:
                    strs += s

            elif mode == READ_PROC:

                # 引数の個数チェック
                if function.function_type == Function.TYPE_OP_FRONT or Function.TYPE_OP_BACK:
                    if len(function.parameters) != 1:
                        ParameterCountError(need=1, fun=function.name)
                elif function.function_type == Function.TYPE_OP_MID:
                    if len(function.parameters) != 2:
                        ParameterCountError(need=2, fun=function.name)

                index = self.__read_process(index=index, function=function)
                success = True
                break

            index += 1

        if not success:
            EOFError(index, info="関数が終了しませんでした").throw()

        if function.name in parent.functions:
            FunctionAlreadyUsedError(index, name=function.name).throw()

        parent.functions[function.name] = function

        return index

    # 式を一つ読む
    def __read_formula(self, *, index, formula, endIndex=None):

        if endIndex == None:
            endIndex = self.program_len

        SKIP_SPACE = 0
        READ_ONE = 1  # 1文字目を読む
        READ_FORMULA = 2  # 1単語を読む
        mode = SKIP_SPACE

        strs = ""
        success = False

        while index < endIndex:
            s = self.program[index]
            is_space = self.is_space(s)

            self.debug("formula", index, s, mode)
            success = False

            if mode == SKIP_SPACE:

                if is_space:
                    pass
                else:
                    mode = READ_ONE
                    continue

            elif mode == READ_ONE:

                if s in String.SYMBOL:

                    # 文字を呼んで追加する
                    res = self.__read_str(index=index + 1, startWith=s)
                    index, value = res[0], res[1]

                    formula.value = value
                    success = True
                    break

                elif s == "(":

                    # 式を追加
                    br_formula = Formula(value=[])
                    index = self.__read_process(
                        index=index+1, function=br_formula, bracket_mode=True)
                    formula.value = br_formula
                    success = True
                    break

                else:
                    mode = READ_FORMULA
                    continue
            elif mode == READ_FORMULA:

                if is_space:

                    if strs == "":
                        pass
                    else:

                        if not Variable.check_name(strs):
                            VariableNameError(index, variable=strs).throw()

                        formula.value = Variable(strs)
                        success = True
                        break

                elif s == "(":

                    if not Variable.check_name(strs):
                        VariableNameError(index, variable=strs).throw()

                    runnable = Runnable(strs)
                    index = self.__read_process(
                        index=index+1, function=runnable, bracket_mode=True)
                    formula.value = runnable
                    success = True

                    break

                else:
                    strs += s

            index += 1

        if not success:
            if mode == READ_FORMULA and strs != "":

                if not Variable.check_name(strs):
                    VariableNameError(index, variable=strs).throw()

                formula.value = Variable(strs)

            else:
                self.debug("実行されないはずの処理")
                return False

        return index

    # 処理を読む
    def __read_process(self, *, index, function, bracket_mode=False):

        SKIP_SPACE = 0
        READ_ONE = 1  # 1文字目を読む
        READ_FORMULA = 2  # 1単語を読む
        mode = SKIP_SPACE

        strs = ""
        start_index = index  # 式の開始地点

        success = False

        while index < self.program_len:
            s = self.program[index]
            is_space = self.is_space(s)

            self.debug("proc", index, s, mode)

            if mode == SKIP_SPACE:

                if is_space:
                    pass
                else:
                    mode = READ_ONE
                    start_index = index
                    continue

            elif mode == READ_ONE:

                if s in String.SYMBOL:

                    # 式を追加
                    formula = Formula()
                    index = self.__read_formula(
                        index=index, formula=formula)

                    if bracket_mode:
                        function.value.append(formula)
                    else:
                        function.process.append(formula)

                    # 戻る
                    mode = SKIP_SPACE
                    strs = ""

                elif s == "(":

                    # 式を追加
                    formula = Formula(value=[])
                    index = self.__read_process(
                        index=index+1, function=formula, bracket_mode=True)

                    if bracket_mode:
                        function.value.append(formula)
                    else:
                        function.process.append(formula)

                    # 戻る
                    mode = SKIP_SPACE
                    strs = ""

                else:

                    if bracket_mode and s == ")":
                        success = True
                        break

                    # 読む
                    mode = READ_FORMULA
                    strs = s

            elif mode == READ_FORMULA:

                if is_space or s == "(":

                    # 関数関連の予約語
                    if strs in Function.SYMBOL:

                        if bracket_mode:
                            ParseError(
                                start_index, reason="括弧の中で関数の宣言、終了は出来ません")

                        # 同名の関数は存在しない
                        if not is_space:
                            VariableKeywordError(index, variable=strs).throw()

                        # end で終了
                        if strs == "end":
                            success = True
                            break

                        index = self.__read_fun(index=index, parent=function,
                                                function_type=Function.symbol2type(strs))

                    else:

                        # 式を追加
                        formula = Formula()
                        index = self.__read_formula(
                            index=start_index, formula=formula)

                        if bracket_mode:
                            function.value.append(formula)
                        else:
                            function.process.append(formula)

                    # 戻る
                    mode = SKIP_SPACE
                    strs = ""

                elif s == ")" and bracket_mode:
                    if strs != "":
                        # 式を追加
                        formula = Formula()
                        index = self.__read_formula(
                            index=start_index, formula=formula, endIndex=index)

                        if bracket_mode:
                            function.value.append(formula)
                        else:
                            function.process.append(formula)
                    # 戻る
                    mode = SKIP_SPACE
                    success = True
                    break
                else:

                    strs += s

            index += 1

        if not success:

            # endで終了、mainなら無視
            if strs == "end":
                pass
            elif mode == READ_FORMULA or mode == READ_ONE:

                # 式を追加
                formula = Formula()
                index = self.__read_formula(
                    index=start_index, formula=formula)

                if bracket_mode:
                    function.value.append(formula)
                else:
                    function.process.append(formula)

            elif function == self.main:
                pass
            else:
                EOFError(index, info=(
                    "括弧" if bracket_mode else "関数")+"が終了しませんでした").throw()

        return index

    # 文字を読む
    def __read_str(self, *, index, startWith):

        READ_STR = 0
        mode = READ_STR

        # 設定
        string = String()
        strs = ""
        ignore_start = False

        success = False

        for index in range(index, len(self.program)):
            if mode == READ_STR:
                s = self.program[index]

                self.debug("s", index, s, ignore_start)

                if s == "\\":
                    if ignore_start:
                        strs += "\\"
                    ignore_start = True
                elif s == startWith:
                    if ignore_start:
                        strs += startWith
                        ignore_start = False
                    else:
                        string.string = strs
                        success = True
                        break
                else:
                    if ignore_start:
                        ignore_start = False
                        strs += "\\"
                    strs += s

        if not success:
            EOFError(index, info="文字が終了しませんでした").throw()

        return [index, string]
