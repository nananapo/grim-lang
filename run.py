from grim.test.debugrun import DebugAndRun
from grim.parser.interpreter import Parser

def run():
    DebugAndRun.run(file = open("grim/test/debug.grim", encoding="utf-8"), debug = False, running =  True)
    #parser = Parser()
    #parser.read()
    #GrimRunner(parser).run()

if __name__ == "__main__":
    run()
