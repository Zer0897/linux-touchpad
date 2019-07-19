from linux_touchpad.watchdog import WatchDog


def test_no_mice_touchpad_enabled(monkeypatch, touchpad):
    monkeypatch.setattr('linux_touchpad.watchdog.is_mouse', lambda *_: False)

    watchdog = WatchDog()
    watchdog._WatchDog__refresh_devices()
    watchdog._WatchDog__update_touchpad()

    assert not watchdog._mice and watchdog._touchpads
    for touchpad in watchdog._touchpads:
        assert touchpad.enabled


def test_has_mice_touchpad_disabled(monkeypatch, touchpad):
    monkeypatch.setattr('linux_touchpad.watchdog.is_mouse', lambda *_: True)

    watchdog = WatchDog()
    watchdog._WatchDog__refresh_devices()
    watchdog._WatchDog__update_touchpad()

    assert watchdog._mice and  watchdog._touchpads
    for touchpad in watchdog._touchpads:
        assert not touchpad.enabled


def test_toggle_touchpad_enabled(monkeypatch, touchpad):
    monkeypatch.setattr('linux_touchpad.watchdog.is_mouse', lambda *_: True)

    watchdog = WatchDog()
    watchdog._WatchDog__refresh_devices()
    watchdog._WatchDog__update_touchpad()

    assert watchdog._mice and watchdog._touchpads
    watchdog.toggle_touchpad()
    for touchpad in watchdog._touchpads:
        assert touchpad.enabled
