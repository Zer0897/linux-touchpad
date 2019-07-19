import pytest
from linux_touchpad.touchpad import TouchPad


@pytest.fixture
def touchpad(monkeypatch):

    class MonkeyTouchPad(TouchPad):
        _enabled = True

        def enable(self):
            self._enabled = True

        def disable(self):
            self._enabled = False

        @property
        def enabled(self):
            return self._enabled

    monkeypatch.setattr('linux_touchpad.watchdog.TouchPad', MonkeyTouchPad)
    return MonkeyTouchPad
