import os
from filelock import FileLock
from pathlib import Path

SRC = Path(__file__).parent

if os.environ.get('DEBUG'):
    lockdir = SRC
else:
    lockdir = Path('/tmp')

pidfp: Path = SRC / '.pid'
lockfp: Path = lockdir / 'linux-touchpad.lock'
lock = FileLock(str(lockfp), timeout=1)
