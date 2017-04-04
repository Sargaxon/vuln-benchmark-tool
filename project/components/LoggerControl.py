import os
from subprocess import call


def start_logging():
    call(["mitmdump", "-s", "%s/Logger.py" % os.path.dirname(os.path.realpath(__file__)), "-p", "9999"])


def stop_logging():
    print("stopped")
