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
    choices = {
        'start': start,
        'toggle': signal_toggle,
        'kill': signal_kill
    }
    parser = argparse.ArgumentParser(
        prog="linux-touchpad",
        description="Auto disable touchpad when mouse is detected."
    )
    parser.add_argument('command', choices=choices)
    args = parser.parse_args()
    command = choices[args.command]
    command()


if __name__ == '__main__':
    main()
