from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser

def test_grim(capfd):
    parser = Parser(open("grim/test/testprogram.grim", encoding="utf-8"))
    parser.read()
    GrimRunner(parser).run()

    #pytest
    out, err = capfd.readouterr()
    out = out.split("\n")

    want = [
        "print string test",

        "assign test1",
        "assign test2",

        "op1 test1",

        "front 2",
        "mid 3",
        
        "\"",
        "'",
    ]

    for i in range(0,len(want)):
        assert out[i] == want[i]