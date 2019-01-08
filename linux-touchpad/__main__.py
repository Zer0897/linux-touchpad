import sys
import os
import asyncio as aio
import signal

from . import lock

from .touchpad import SIGTOGGLE, watchdevices
from .process import handler


def start():
    with lock.lock():
        signal.signal(signal.SIGTERM, handler)
        signal.signal(SIGTOGGLE, handler)

        aio.run(watchdevices())


def signal_toggle():
    pid = lock.getuid()
    os.kill(pid, SIGTOGGLE)


def signal_kill():
    pid = lock.getuid()
    os.kill(pid, signal.SIGTERM)


options = {
    'start': start,
    'toggle': signal_toggle,
    'kill': signal_kill
}


if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] not in options:
        raise TypeError("Invalid arguments")

    command = options.get(sys.argv[1])
    command()
