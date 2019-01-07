import os
import sys
import asyncio as aio
import signal
from contextlib import suppress

from .touchpad import SIGTOGGLE, toggle, watchdevices

path, _ = os.path.split(__file__)


class Lock:

    _lock = os.path.join(path, '.lock')

    def __enter__(self):
        self.lock()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.unlock()

    def lock(self):
        assert not self.locked
        with open(self._lock, 'w+') as fp:
            fp.write(str(os.getpid()))

    def unlock(self):
        os.remove(self._lock)

    def kill(self, signum, frame):
        with suppress(FileNotFoundError):
            self.unlock()
        sys.exit()

    @property
    def locked(self):
        return os.path.exists(self._lock)

    @classmethod
    def get_process(cls):
        with open(cls._lock) as fp:
            return int(fp.read())


def start():
    with Lock() as lock:
        signal.signal(signal.SIGTERM, lock.kill)
        signal.signal(SIGTOGGLE, toggle)

        aio.run(watchdevices())


def signal_toggle():
    pid = Lock.get_process()
    signal.pthread_kill(pid, SIGTOGGLE)


options = {
    'start': start,
    'toggle': signal_toggle
}


if __name__ == '__main__':

    if len(sys.argv) != 2 or sys.argv[1] not in options:
        raise TypeError("Invalid arguments")

    command = options.get(sys.argv[1])
    command()
