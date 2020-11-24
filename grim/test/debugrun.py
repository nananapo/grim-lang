
from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser


class DebugAndRun:

    @staticmethod
    def run(file, debug=False, running=True, logfile=None):

        if debug:
            print("========Parse==========", file=logfile)

        parser = Parser(file, debug, logfile=logfile)
        parser.read()

        if debug:
            print(file=logfile)
            print("========ParseResult==========", file=logfile)

            print(file=logfile)
            print("--Formulas in <main>--", file=logfile)
            for formula in parser.main.process:
                print(formula, file=logfile)

            print(file=logfile)
            print("--Functions in <main>--", file=logfile)
            for name in parser.main.functions:
                fun = parser.main.functions[name]
                print(fun, file=logfile)
                print("   ", "params:", fun.parameters, file=logfile)
                print("   ", "---functions---", file=logfile)
                for fn2 in fun.functions:
                    print("       ", fun.functions[fn2], file=logfile)
                print("   ", "---process---", file=logfile)
                for value in fun.process:
                    print("       ", value, file=logfile)

            if running:
                print("========RUNNING========", file=logfile)

        if running:
            GrimRunner(parser, enable_debug=debug, logfile=logfile).run()
