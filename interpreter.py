
"""
いきなり-,op - はマイナス
全ては値渡し
"""

import sys
import vm


class Parser:

    def __init__(self, string):
        self.program = string
        self.program_len = len(self.program)
        self.main = NameSpace("main", NameSpace.ROOT)

    # read
    def read(self, i=0):
        self.__read_proc(i, self.main)

    # 区切りを判別
    def is_space(self, string):
        return string == " " or string == "\n"

    # funを読む
    """
    関数を定義するワード : fun
    
    fun 関数名(引数1,引数2,・・・)
        処理
    end

    引数が無い場合は括弧をスキップできる
    
    ,,,とか書いても無視されます => 厳格にするかも

    """

    def __read_fun(self, i, parent, namespace):

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

                    # 予約語もダメ TODO 記号禁止
                    if strs == "fun" or strs == "end" or ":" in strs:
                        VariableNameError(strs, parent.name, i).throw()

                    if namespace == None:
                        namespace = NameSpace(strs, parent)

                    namespace.name = strs
                    namespace.parent = parent

                    mode = READ_PARAMS_BRACKET
                    strs = ""

                elif s == "(":

                    # 名前被りはダメ
                    if strs in parent.functions:
                        FunctionAlreadyUsedError(strs, i).throw()

                    # 予約語もダメ TODO 記号禁止
                    if strs == "fun" or strs == "end" or ":" in strs:
                        VariableNameError(strs, parent.name, i).throw()

                    if namespace == None:
                        namespace = NameSpace(strs, parent)

                    namespace.name = strs
                    namespace.parent = parent

                    mode = READ_PARAMS
                    strs = ""
                
                #:は禁止
                elif s == ":":
                    VariableNameError(strs + s, parent.name, i).throw()
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
                    pass
                elif s == ")":

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in namespace.parameters:
                            ParameterNameError(strs, parent.name, i).throw()

                        # 予約語もダメ TODO 記号禁止
                        if strs == "fun" or strs == "end":
                            VariableNameError(strs, parent.name, i).throw()

                        # 追加
                        namespace.parameters.append(strs)
                        strs = ""

                    mode = READ_PROC

                elif s == ",":

                    if strs != "":

                        # 同じ名前の引数はエラーを出す
                        if strs in namespace.parameters:
                            ParameterNameError(strs, parent.name, i).throw()

                        # 予約語もダメ TODO 四則演算禁止
                        if strs == "fun" or strs == "end":
                            VariableNameError(strs, parent.name, i).throw()

                        # 追加
                        namespace.parameters.append(strs)
                        strs = ""

                    else:
                        # 何もない場合はスキップ
                        pass

                #:は禁止
                elif s == ":":
                    VariableNameError(strs + s, parent.name, i).throw()
                    
                else:
                    strs += s
            elif mode == READ_PROC:
                i = self.__read_proc(i+1, namespace)
                success = True
                break

            i += 1

        if not success:
            EOFError(i).throw()

        return i-1

    # funを呼ぶときの引数を読む
    """
    全て式
    ex
    式,式

    式以降に値を入れたら無視される
    ex
    式1 式2,式3

    =>式2は無視
    """

    def __read_fun_params(self, i, namespace, runnable):

        READ_BASE = 0
        READ_FORMULA = 1
        mode = READ_BASE

        formula_index = i
        bracket_size = 0  # (+1 )-1

        success = False

        while i < self.program_len:
            s = self.program[i]
            is_space = self.is_space(s)

            print("fp", i, s, mode)

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
                elif s == ",":
                    ParseError(i).throw()
                else:
                    formula_index = i
                    mode = READ_FORMULA

            elif mode == READ_FORMULA:
                if is_space:
                    pass
                elif s == "(":
                    bracket_size += 1
                elif s == ")":
                    if bracket_size == 0:
                        formula = Formula()
                        self.__read_formula_value(
                            formula_index, namespace, formula, endIndex=i)
                        runnable.parameters.append(formula)
                        success = True
                        break
                    else:
                        bracket_size -= 1
                elif s == ",":
                    formula = Formula()
                    self.__read_formula_value(
                        formula_index, namespace, formula, endIndex=i)
                    runnable.parameters.append(formula)
                    mode = READ_BASE
                else:
                    pass
            i += 1

        if not success:
            EOFError(i).throw()

        return i

    # 式の値を読む
    """
    関数を呼ぶときは引数が無い場合スキップできる,引数アリのときの指定は(の前にスペースがあってはいけない
    endIndex はexclusive
    """

    def __read_formula_value(self, i, parent, formula=None, endIndex=None):

        if endIndex == None:
            endIndex = self.program_len

        if formula == None:
            formula = Formula()

        #print("formula", i, endIndex)

        if i == endIndex:
            return endIndex

        READ_VALUE = 0
        READ_OP = 1
        READ_VALUE_MUST = 2
        mode = READ_VALUE

        strs = ""
        value_index = i

        success = False

        while i < endIndex:
            s = self.program[i]
            is_space = self.is_space(s)

            print("f", i, s, mode,parent.name)

            success = False

            if mode == READ_VALUE:
                if is_space:
                    if strs == "":
                        pass
                    else:

                        if strs == "end":
                            ParseError(i).throw()

                        elif strs == "fun":

                            namespace = NameSpace("undefined", parent)
                            i = self.__read_fun(i+1, parent, namespace)
                            parent.functions[namespace.name] = namespace
                            strs = ""
                            success = True
                            break

                        else:

                            # :だけはだめ
                            if strs == ":":
                                VariableNameError(strs, parent.name, i).throw()

                            formula.value.append(Variable(strs))
                            strs = ""
                            mode = READ_OP
                            success = True

                elif s == "=":
                    ParseError(i).throw()

                # " => 文字
                elif s in String.SYMBOL:
                    # 文字を呼んで追加する
                    res = self.__read_str(i+1, s)
                    i, string = res[0], res[1]
                    formula.value.append(string)

                    strs = ""
                    mode = READ_OP
                    success = True
                # op
                elif s in Operator.SYMBOL:

                    # 空なのにいきなり演算子がきたらエラー
                    if strs == "":
                        ParseError(i).throw()

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, parent.name, i).throw()

                    formula.value.append(Variable(strs))
                    formula.value.append(Operator(s))

                    strs = ""
                elif s == "(":

                    # 空なのにいきなり(がきたらエラー
                    if strs == "":
                        ParseError(i).throw()

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, parent.name, i).throw()

                    runnable = Runnable(strs)
                    i = self.__read_fun_params(i+1, parent, runnable)
                    formula.value.append(runnable)

                    strs = ""
                    mode = READ_OP
                    success = True
                else:
                    strs += s

            elif mode == READ_OP:
                if is_space:
                    pass
                elif s == "=":
                    ParseError(i).throw()
                # op => 文字を読む
                elif s in Operator.SYMBOL:
                    formula.value.append(Operator(s))
                    mode = READ_VALUE_MUST
                    value_index = i
                else:
                    # 終了
                    success = True
                    break
            elif mode == READ_VALUE_MUST:

                if is_space:
                    if strs == "":
                        pass
                    # いきなりend,fun
                    if strs == "end" or strs == "fun":
                        ParseError(i).throw()
                    else:
                        i = value_index
                        mode = READ_VALUE

                elif s == "=":
                    ParseError(i).throw()

                # op  TODO マイナス記号
                elif s in Operator.SYMBOL:
                    ParseError(i).throw()

                # 文字開始
                elif s in String.SYMBOL:
                    mode = READ_VALUE
                    continue

                # 関数開始
                elif s == "(":
                    
                    #空
                    if strs == "":
                        ParseError(i).throw()

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, parent.name, i).throw()

                    i = value_index
                    mode = READ_VALUE

                else:
                    strs += s

            i += 1

        print(strs,mode)
        if not success:
            if mode == READ_VALUE:
                if strs != "":
                    formula.value.append(Variable(strs))
                else:
                    EOFError(i).throw()
            else:
                EOFError(i).throw()

        return i-1

    # 処理を読む
    """
    全ての処理は式
    参照する変数 = 式本体
    が基本形(変数=は省略可)
    一連の処理もオブジェクトに => ifとかも
    """

    def __read_proc(self, i, namespace):

        # 状態
        READ_BASE = 0
        READ_ASSIGN = 1
        READ_VALUE_OR_EQUAL = 2
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

                # エラー
                elif s in Operator.SYMBOL:
                    ParseError(i).throw()

                # 文字開始
                elif s in String.SYMBOL:
                    formula = Formula()
                    i = self.__read_formula_value(i, namespace, formula)
                    namespace.process.append(formula)

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
                        VariableNameError(strs, namespace.name, i).throw()

                    mode = READ_VALUE_OR_EQUAL

                # =で代入
                elif s == "=":
                    
                    # 変数名確認
                    if strs == "end" or strs == "fun":
                        VariableNameError(strs, namespace.name, i).throw()
                    
                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, namespace.name, i).throw()

                    # 式を追加
                    formula = Formula(strs)
                    i = self.__read_formula_value(i+1, namespace, formula)
                    namespace.process.append(formula)

                    mode = READ_BASE
                    strs = ""

                # いきなり文字開始
                elif s in String.SYMBOL:

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, namespace.name, i).throw()

                    # 式を追加
                    formula = Formula()
                    i = self.__read_formula_value(
                        assign_index, namespace, formula)
                    namespace.process.append(formula)

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                # 演算子が開始
                elif s in Operator.SYMBOL:

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, namespace.name, i).throw()

                    # 式を追加
                    formula = Formula()
                    i = self.__read_formula_value(
                        assign_index, namespace, formula)
                    namespace.process.append(formula)

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                # 引数ありRunnable
                elif s == "(":

                    # :だけはだめ
                    if strs == ":":
                        VariableNameError(strs, namespace.name, i).throw()
                        
                    # 式を追加
                    formula = Formula()
                    i = self.__read_formula_value(
                        assign_index, namespace, formula)
                    namespace.process.append(formula)

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                else:
                    strs += s
            elif mode == READ_VALUE_OR_EQUAL:
                if is_space:
                    pass
                elif s == "=":

                    # 変数名確認
                    if strs == "end" or strs == "fun":
                        VariableNameError(strs, namespace.name, i).throw()

                    # 式を追加
                    formula = Formula(strs)
                    i = self.__read_formula_value(
                        i+1, namespace, formula)
                    namespace.process.append(formula)

                    mode = READ_BASE
                    strs = ""

                elif s in String.SYMBOL:

                    # 式を追加
                    formula = Formula()
                    i = self.__read_formula_value(
                        assign_index, namespace, formula)
                    namespace.process.append(formula)

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                elif s in Operator.SYMBOL:

                    # 式を追加
                    formula = Formula()
                    i = self.__read_formula_value(
                        assign_index, namespace, formula)
                    namespace.process.append(formula)

                    # 戻る
                    mode = READ_BASE
                    strs = ""

                else:
                    # 関数終了
                    if strs == "end":
                        success = True
                        break

                    else:
                        # 式を追加
                        formula = Formula()
                        i = self.__read_formula_value(
                            assign_index, namespace, formula)

                        if strs != "fun":
                            namespace.process.append(formula)

                        # 戻る
                        mode = READ_BASE
                        strs = ""

            i += 1

        if not success:
            # endで終了の場合もある
            if strs == "end":
                pass
            elif namespace == self.main:
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
                #print("s", i, s)
                if s == startWith:
                    string.string = strs
                    success = True
                    break
                else:
                    strs += s

        if not success:
            EOFError(i).throw()

        return [i, string]


class NameSpace:  # 名前空間

    ROOT = 0

    def __init__(self, name, parent):
        self.name = name
        self.process = []
        self.parameters = []
        self.functions = {}
        self.parent = parent

    def is_root(self):
        return self.parent == NameSpace.ROOT

    def __str__(self):
        return "NameSpace<" + self.name+">"


class Formula:  # 式

    ID = 0

    def __init__(self, assign=None, value=None):
        self.assign = assign
        self.value = value if value != None else []

    def only_value(self):
        return self.assign == None

    def is_dynamic(self):
        return self.assign[0] == ":"

    def get_assign(self):
        return self.assign if not self.is_dynamic() else self.assign[1::]

    def __str__(self):
        return "Formula" + str(self.value)


class Variable:
    TYPE_NONE = -1
    TYPE_VARIABLE = 0
    TYPE_RUNNABLE = 1
    TYPE_OPERATOR = 2
    TYPE_STRING = 3
    TYPE_NUMERIC = 4

    def __init__(self, name):
        self.name = name
        self.value = None

    def get_type(self):
        return Variable.TYPE_VARIABLE

    def is_dynamic(self):
        return self.name[0] == ":"

    def get_assign(self):
        return self.name if not self.is_dynamic() else self.name[1::]

    def __str__(self):
        return "Variable<"+self.name+">"


class VariableNone(Variable):

    def __init__(self):
        pass

    def get_type(self):
        return Variable.TYPE_NONE

    def __str__(self):
        return "VariableNone"


class Runnable(Variable):  #
    def __init__(self, name, params=None):
        self.name = name
        self.parameters = params if params != None else []

    def __str__(self):
        return "Runnable<"+self.name+">" + str(self.parameters)

    def get_type(self):
        return Variable.TYPE_RUNNABLE


class Operator:
    SYMBOL = ["+", "-", "*", "/", "%"]
    SYMBOL_DICT = {
        "+": 1,
        "-": 2,
        "*": 3,
        "/": 4
    }

    def __init__(self, op):
        self.operator = op

    def get_type(self):
        return Variable.TYPE_OPERATOR

    def get_op(self):
        return Operator.SYMBOL_DICT[self.operator]

    def __str__(self):
        return "Operator<"+self.operator + ">"


class String:
    SYMBOL = ["\"", "'"]

    def __init__(self, string=""):
        self.string = string

    def get_type(self):
        return Variable.TYPE_STRING

    def copy(self):
        return String(self.string)

    def __str__(self):
        return self.string

    def __add__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            return String(self.string+str(other.number))
        elif o_type == Variable.TYPE_STRING:
            return String(self.string+other.string)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "+").throw()

    def __sub__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NONE:
            return self.copy()
        vm.UnknownOperationError(self, other, "-").throw()

    def __mul__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            return Numeric(self.string*other.number)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "*").throw()

    def __truediv__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NONE:
            return self.copy()
        vm.UnknownOperationError(self, other, "/").throw()


class Numeric:
    __NUMBER = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"])

    def __init__(self, number):
        self.number = number

    def get_type(self):
        return Variable.TYPE_NUMERIC

    def copy(self):
        return Numeric(self.number)

    # 文字列が数字か判定 -> False or 数値
    @staticmethod
    def is_num(string):

        front = False
        point = False
        for s in string:
            if not point:
                if s == "+" or s == "-":
                    if front:
                        return False
                    front = True
                elif s == ".":
                    point = True
                elif s in Numeric.__NUMBER:
                    pass
                else:
                    return False
            else:
                if s == "+" or s == "-":
                    return False
                elif s == ".":
                    return False
                elif s in Numeric.__NUMBER:
                    pass
                else:
                    return False
        return float(string) if point else int(string)

    def __str__(self):
        return str(self.number)

    def __add__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            return Numeric(self.number+other.number)
        elif o_type == Variable.TYPE_STRING:
            return String(str(self.number)+other.string)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "+").throw()

    def __sub__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            return Numeric(self.number-other.number)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "-").throw()

    def __mul__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            return Numeric(self.number*other.number)
        elif o_type == Variable.TYPE_STRING:
            return String(self.number*other.string)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "*").throw()

    def __truediv__(self, other):
        o_type = other.get_type()
        if o_type == Variable.TYPE_NUMERIC:
            if other.number == 0:
                vm.ZeroDivisionError().throw()
            return Numeric(self.number/other.number)
        elif o_type == Variable.TYPE_NONE:
            return self.copy()
        else:
            vm.UnknownOperationError(self, other, "/").throw()


class ParseError:
    def __init__(self, index=0):
        index = str(index)
        self.error = "ParseError :インデックス " + index

    def name(self):
        return "ParseError"

    def throw(self):
        print("構文解析中にエラーが発生しました : ", self.name())
        print(self.error)
        exit()


class ParameterNameError(ParseError):

    def __init__(self, param, def_id, index):
        index = str(index)
        self.error = "引数名 " + param + " は既に使用されています :関数名 " + def_id + " :インデックス " + index

    def name(self):
        return "ParameterNameError"


class FunctionAlreadyUsedError(ParseError):

    def __init__(self, def_id, index):
        index = str(index)
        self.error = "関数名 " + def_id + " は既に使用されています :インデックス "+index

    def name(self):
        return "FunctionAlreadyUsedError"


class EOFError(ParseError):

    def __init__(self, index):
        index = str(index)
        self.error = "構文解析中にファイルが終了しました :インデックス "+index

    def name(self):
        return "EOFError"


class VariableNameError(ParseError):

    def __init__(self, variable, def_id, index):
        index = str(index)
        self.error = "変数名 " + variable + \
            " は予約語として既に使用されています :関数名 " + def_id + " :インデックス " + index

    def name(self):
        return "VariableNameError"


if __name__ == "__main__":

    sys.setrecursionlimit(10000)

    debug = True

    # get filename
    filepath = "ex1.grim"  # input()
    lines = open(filepath).readlines()

    program = ""
    for line in lines:
        program += line

    parser = Parser(program)
    parser.read()

    if debug:
        print("========ParseResult==========")
        for formula in parser.main.process:
            print("formula<", formula.assign, ">")
            for value in formula.value:
                print("   ", value)
        for name in parser.main.functions:
            fun = parser.main.functions[name]
            print("NameSpace<", name, ">")
            print("   ", "params:", fun.parameters)
            print("   ", "---functions---")
            for fn2 in fun.functions:
                print("       ", fun.functions[fn2])
            print("   ", "---process---")
            for value in fun.process:
                print("       ", value)
        print("========RUNNING========")
    vm.GrimVM(parser).run()
