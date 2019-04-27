import os
import signal
import argparse

from .lock import Lock
from .touchpad import SIGTOGGLE
from .watchdog import WatchDog


def start():
    with Lock():
        watchdog = WatchDog()
        signal.signal(signal.SIGTERM, watchdog.sig_handler)
        signal.signal(SIGTOGGLE, watchdog.sig_handler)
        watchdog.start()


def signal_toggle():
    pid = Lock.getpid()
    os.kill(pid, SIGTOGGLE)


def signal_kill():
    if Lock.islocked():
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
