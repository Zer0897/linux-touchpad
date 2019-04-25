import os
import asyncio as aio
import signal
import argparse

from .lock import Lock, LockExistsError
from .touchpad import SIGTOGGLE, watch_devices
from .process import handler


def start():
    try:
        with Lock():
            signal.signal(signal.SIGTERM, handler)
            signal.signal(SIGTOGGLE, handler)

            aio.run(watch_devices())

    except LockExistsError:
        pass


def signal_toggle():
    pid = Lock.getpid()
    os.kill(pid, SIGTOGGLE)


def signal_kill():
    pid = Lock.getpid()
    os.kill(pid, signal.SIGTERM)


def main():
    options = {
        'start': start,
        'toggle': signal_toggle,
        'kill': signal_kill
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('command')

    args = parser.parse_args()
    command = options.get(args.command)
    if command is not None:
        command()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
