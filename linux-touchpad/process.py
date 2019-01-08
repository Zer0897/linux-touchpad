import signal

from . import lock
from .touchpad import SIGTOGGLE, toggle


def handler(signum, frame):
    command = sigmap.get(signum)
    if command:
        command()
    else:
        lock.cleanup()


sigmap = {
    signal.SIGKILL: lock.cleanup,
    SIGTOGGLE: toggle
}
