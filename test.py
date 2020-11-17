import sys
from grim.test.runtest import Tester

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    Tester().run("./grim/test/test.grim")
