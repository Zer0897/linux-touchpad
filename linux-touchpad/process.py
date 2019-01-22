import os
from contextlib import suppress
from . import touchpad as tp


def handler(signum, frame):
    if signum == tp.SIGTOGGLE:
        tp.toggle()
    else:
        tp.kill()


def kill(ps):
    with suppress(ProcessLookupError):
        os.kill(ps, 9)
