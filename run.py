from grim.test.debugrun import DebugAndRun

def run():
    DebugAndRun.run(file=open("grim/test/debug.grim", encoding="utf-8"), debug=True, running=True)


if __name__ == "__main__":
    run()
