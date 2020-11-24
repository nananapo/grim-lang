from grim.test.debugrun import DebugAndRun
import sys


def run():
    name = "sample/bubblesort.grim"
    # name = "grim/test/testprogram.grim"
    DebugAndRun.run(file=open(name, encoding="utf-8"),
                    debug=True, running=True, logfile=open("debug_msg.txt", mode="w",encoding="utf-8"))


if __name__ == "__main__":
    sys.setrecursionlimit(10000000)
    run()
