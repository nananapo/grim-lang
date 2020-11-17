

from ..parser.interpreter import Parser
from ..vm.grimvm import GrimRunner

class Tester:

    def run(self,filepath):
        
        lines = open(filepath, encoding="utf-8").readlines()

        program = ""
        for line in lines:
            program += line

        parser = Parser(program)
        parser.read()

        if False:
            print("========ParseResult==========")

            for formula in parser.main.process:
                print(formula)

            for name in parser.main.functions:
                fun = parser.main.functions[name]
                print(fun)
                print("   ", "params:", fun.parameters)
                print("   ", "---functions---")
                for fn2 in fun.functions:
                    print("       ", fun.functions[fn2])
                print("   ", "---process---")
                for value in fun.process:
                    print("       ", value)
                    
            print("========RUNNING========")

        GrimRunner(parser).run()
