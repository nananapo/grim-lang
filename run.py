from grim.test.debugrun import DebugAndRun
import sys


def run():
    # name = "sample/array.grim"
    name = "grim/test/testprogram.grim"
    DebugAndRun.run(file=open(name, encoding="utf-8"),
                    debug=False, running=True)


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    run()
