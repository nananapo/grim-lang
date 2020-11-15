import sys

from grim.parser.interpreter import Parser
from grim.vm.grimvm import GrimRunner

if __name__ == "__main__":

    sys.setrecursionlimit(10000)

    debug = True

    # get filename
    filepath = "./grim/example/ex1.grim"  # input()
    lines = open(filepath).readlines()

    program = ""
    for line in lines:
        program += line

    parser = Parser(program)
    parser.read()

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
    GrimRunner(parser).run()
