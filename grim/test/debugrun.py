
from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser

class DebugAndRun:

    def run(self,file,debug = False):
        
        if debug:
            print("========Parse==========")

        parser = Parser(file, debug)
        parser.read()

        if debug:
            print()
            print("========ParseResult==========")

            print()
            print("--Formulas in <main>--")
            for formula in parser.main.process:
                print(formula)

            print()
            print("--Functions in <main>--")
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