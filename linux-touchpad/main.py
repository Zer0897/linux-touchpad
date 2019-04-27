import os
import signal
import argparse

from .lock import Lock
from .touchpad import SIGTOGGLE
from .watchdog import WatchDog


def start():
    with Lock() as lock:
        watchdog = WatchDog()
        signal.signal(signal.SIGTERM, lambda *args: lock.cleanup())
        signal.signal(SIGTOGGLE, watchdog.on_toggle)
        watchdog.start()


def signal_toggle():
    if Lock.is_locked():
        pid = Lock.get_pid()
        os.kill(pid, SIGTOGGLE)


def signal_kill():
    if Lock.is_locked():
        pid = Lock.get_pid()
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
