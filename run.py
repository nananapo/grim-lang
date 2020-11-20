from grim.test.debugrun import DebugAndRun

def run():
    DebugAndRun.run(file=open("grim/test/testprogram.grim", encoding="utf-8"), debug=False, running=True)


if __name__ == "__main__":
    run()
