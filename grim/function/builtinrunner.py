from grim.vm.runstack import SearchResult
from grim.error.vmerror import ParameterNotMatchError, VMError, VariableNotFoundError, NumericCastError, TypeError
from grim.formula.variable import VariableNone
from grim.formula.primitive import Boolean, Numeric, String
from grim.formula.types import ClassType


class BuiltInRunner:

    @staticmethod
    def run_builtin(name, params, runstack):

        param_len = len(params)
        result = None

        if name == "input":
            print(*params)
            result = String(input())
        elif name == "print":
            print(*params)
            result = VariableNone()
        elif name == "return":
            result = params
        elif name == "__assign":

            if param_len != 2:
                ParameterNotMatchError("__assign").throw()

            type0 = params[0].get_type()
            varname = ""
            if type0 == ClassType.TYPE_NAME or type0 == ClassType.TYPE_INDEFINITE:
                varname = params[0].name
            elif type0 == ClassType.TYPE_STRING:
                varname = params[0].string
            elif type0 == ClassType.TYPE_NUMERIC:
                varname = str(params[0].number)
            else:
                ParameterNotMatchError("__assign").throw()

            search_result = runstack.search_variable(
                varname, variable_only=True)

            if search_result.result == SearchResult.RESULT_VARIABLE:
                search_result.variables[varname] = params[1]
            else:
                VariableNotFoundError(varname).throw()

            result = params[1]

        elif name == "__plus":

            if param_len != 2:
                ParameterNotMatchError("__plus").throw()
            result = params[0] + params[1]

        elif name == "__minus":

            if param_len != 2:
                ParameterNotMatchError("__minus").throw()
            result = params[0] - params[1]

        elif name == "__mul":

            if param_len != 2:
                ParameterNotMatchError("__mul").throw()
            result = params[0] * params[1]

        elif name == "__div":

            if param_len != 2:
                ParameterNotMatchError("__div").throw()
            result = params[0] / params[1]

        elif name == "__num":

            if not(params[0].get_type() == ClassType.TYPE_STRING):
                ParameterNotMatchError("__num").throw()

            num = Numeric.is_num(params[0].string)
            if isinstance(num, bool):
                NumericCastError(params[0].string).throw()

            result = Numeric(num)

        elif name == "__str":

            if not(params[0].get_type() == ClassType.TYPE_NUMERIC):
                ParameterNotMatchError("__num").throw()

            result = Numeric(str(params[0].number))

        elif name == "__true" or name == "__false":

            if param_len != 0:
                ParameterNotMatchError("__true").throw()

            result = Boolean(True) if name == "__true" else Boolean(False)

        elif name == "__equal":

            if param_len != 2:
                ParameterNotMatchError("__plus").throw()

            type0 = params[0].get_type()
            # 型が一致しないとfalse
            if type0 != params[1].get_type():
                result = Boolean(False)
            else:
                if type0 == ClassType.TYPE_STRING:
                    result = Boolean(params[0].string == params[1].string)
                elif type0 == ClassType.TYPE_NUMERIC:
                    result = Boolean(params[0].number == params[1].number)
                elif type0 == ClassType.TYPE_BOOLEAN:
                    result = Boolean(params[0].value == params[1].value)
                else:
                    result = Boolean(False)

        elif name == "__larger":

            if param_len != 2:
                ParameterNotMatchError("__larger").throw()

            type0 = params[0].get_type()
            # 型はnumberのみ
            if type0 != params[1].get_type() or type0 != ClassType.TYPE_NUMERIC:
                TypeError("__largerの引数は数値である必要があります。").throw()

            result = Boolean(params[0].number > params[1].number)

        elif name == "__type":

            if param_len != 1:
                ParameterNotMatchError("__type").throw()

            type0 = params[0].get_type()

            if type0 == ClassType.TYPE_NONE:
                result = "VariableNone"
            elif type0 == ClassType.TYPE_STRING:
                result = "String"
            elif type0 == ClassType.TYPE_NUMERIC:
                result = "Numeric"
            elif type0 == ClassType.TYPE_BOOLEAN:
                result = "Boolean"
            elif type0 == ClassType.TYPE_INDEFINITE:
                result = "Indefinite"
            elif type0 == ClassType.TYPE_NAME:
                result = "Name"
            else:
                result = "Unknown"
            
            result = String(string=result)

        return result
