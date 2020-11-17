from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser

def run():
    parser = Parser(open("grim/test/testprogram.grim", encoding="utf-8"))
    parser.read()
    GrimRunner(parser).run()

if __name__ == "__main__":
    run()