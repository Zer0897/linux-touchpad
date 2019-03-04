import sys
import os
import asyncio as aio
import signal

from .lock import Lock, LockExistsError
from .touchpad import SIGTOGGLE, watchdevices
from .process import handler


def start():
    try:
        with Lock():
            signal.signal(signal.SIGTERM, handler)
            signal.signal(SIGTOGGLE, handler)

            aio.run(watchdevices())

    except LockExistsError:
        pass


def signal_toggle():
    pid = Lock.getpid()
    os.kill(pid, SIGTOGGLE)


def signal_kill():
    pid = Lock.getpid()
    os.kill(pid, signal.SIGTERM)


options = {
    'start': start,
    'toggle': signal_toggle,
    'kill': signal_kill
}


if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] not in options:
        print(sys.argv)
        raise TypeError("Invalid arguments")

    command = options.get(sys.argv[1])
    command()
