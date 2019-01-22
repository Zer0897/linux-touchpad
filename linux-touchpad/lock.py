import os
from contextlib import suppress

from .process import kill


class LockExistsError(Exception):
    pass


class Lock:

    path, _ = os.path.split(__file__)
    _lock = os.path.join(path, '.lock')

    def __init__(self):
        if self.islocked():
            lockpid = self.getpid()
            kill(lockpid)
            self.cleanup()

    def __enter__(self):
        self.create_lock()
        return self

    def __exit__(self, *args):
        self.cleanup()

    def create_lock(self):
        with open(Lock._lock, 'w+') as fp:
            fp.write(str(os.getpid()))

    def cleanup(self):
        with suppress(FileNotFoundError):
            os.remove(self._lock)

    @staticmethod
    def islocked() -> bool:
        return os.path.exists(Lock._lock)

    @staticmethod
    def getpid():
        with open(Lock._lock) as fp:
            return int(fp.read())
