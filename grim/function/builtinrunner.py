from ..vm.runstack import SearchResult
from ..error.vmerror import ParameterNotMatchError, VariableNotFoundError
from ..formula.variable import *
from ..formula.primitive import *

class BuiltInRunner:

    @staticmethod
    def run_builtin(name, params,runstack):

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

            if not(params[0].get_type() == ClassType.TYPE_NAME or params[0].get_type() == ClassType.TYPE_INDEFINITE):
                ParameterNotMatchError("__assign").throw()

            search_result = runstack.search_variable(params[0].name,variable_only = True)

            if search_result.result == SearchResult.RESULT_VARIABLE:
                search_result.variables[params[0].name] = params[1]
            else:
                VariableNotFoundError(params[0].name).throw()

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

        return result
