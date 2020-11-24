from grim.vm.grimvm import GrimRunner
from grim.parser.interpreter import Parser


def test_array(capfd):
    parser = Parser(open("grim/test/sample/bubblesort.grim", encoding="utf-8"))
    parser.read()
    GrimRunner(parser).run()

    # pytest
    out, err = capfd.readouterr()
    out = out.split("\n")

    want = [
        "-88 -86 -86 -74 -73 4 6 29 46 47 62 97!"
    ]

    for i in range(0, len(want)):
        assert out[i] == want[i]
