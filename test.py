from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser

def test_program(capfd):
    parser = Parser("./testprogram.grim")
    parser.read()
    GrimRunner(parser).run()

    #pytest
    out, err = capfd.readouterr()
    out = out.split("\n")

    want = [
        "print string test",
        "assign test1",
        "op1 test1",
        "front 2",
        "mid 3",
        "\"",
        "'",
    ]

    for i in range(0,len(want)):
        assert out[i] == want[i]

if __name__ == "__main__":
    parser = Parser("./testprogram.grim")
    parser.read()
    GrimRunner(parser).run()
