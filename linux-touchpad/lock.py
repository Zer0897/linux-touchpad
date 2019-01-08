import os
from contextlib import contextmanager, suppress
from .touchpad import kill

path, _ = os.path.split(__file__)
_lock = os.path.join(path, '.lock')


@contextmanager
def lock():
    already_locked = False
    try:
        create_lock()
        yield getuid

    except AssertionError:
        already_locked = True

    finally:
        if not already_locked:
            cleanup()


def islocked() -> bool:
    return os.path.exists(_lock)


def create_lock():
    assert not islocked()
    with open(_lock, 'w+') as fp:
        fp.write(str(os.getpid()))


def cleanup():
    with suppress(FileNotFoundError):
        os.remove(_lock)
    kill()


def getuid():
    with open(_lock) as fp:
        return int(fp.read())
