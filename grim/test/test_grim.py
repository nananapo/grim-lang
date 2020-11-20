from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser


def test_grim(capfd):
    parser = Parser(open("grim/test/testprogram.grim", encoding="utf-8"))
    parser.read()
    GrimRunner(parser).run()

    # pytest
    out, err = capfd.readouterr()
    out = out.split("\n")

    want = [
        "print string test",
        "assign test1",
        "assign test2",
        "205 : value*2 + 5",
        "op1 test1",
        "front 2",
        "mid 3",
        "back 2.0",
        "\"",
        "'",
        "10",
        "101",
        "1.8",
        "11",
        "2.0",
        "42.0",
        "1.0",
        "68",
        "5",
        "1.0",
        "here",
        "12",
        "6.6",
        "True",
        "False",
        "True",
        "True",
        "True",
        "False",
        "True",
        "False",
        "False",
        "True",
        "False",
        "True",
        "True",
        "True",
        "False",
    ]

    for i in range(0, len(want)):
        assert out[i] == want[i]
