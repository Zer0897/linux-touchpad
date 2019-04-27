import sys
from enum import Enum
from pyudev import Context, Monitor
from collections import defaultdict

from .touchpad import TouchPad, SIGTOGGLE


class DeviceClass(Enum):
    TouchPad = 0
    Mouse = 1
    Other = 2


def identify(device) -> DeviceClass:
    props = look(
        device,
        ('removable', 'removable'),
        ('phys', 'usb'),
    )

    if 'removable' in props:
        return DeviceClass.Mouse

    # USB but not removable probably means it's a controller
    if 'usb' in props:
        return DeviceClass.Other

    return DeviceClass.TouchPad


def look(device, *items) -> set:
    found = set()
    for dev in [device] + list(device.ancestors):
        for name, val in items:
            prop = dev.attributes.get(name)
            if prop and val in prop.decode():
                found.add(name)
    return found


class WatchDog:
    context = Context()
    devices = set()

    _touchpad = None

    def __init__(self):
        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by('input')

        for dev in self.context.list_devices(subsystem='input', sys_name='mouse*'):
            cls = identify(dev)
            if cls is DeviceClass.TouchPad:
                self._touchpad = TouchPad(dev)
            elif cls is DeviceClass.Mouse:
                self.add(dev)

        self.refresh()

    def start(self):
        for device in iter(self.monitor.poll, None):
            if 'mouse' in device.sys_name:
                cls = identify(device)
                if cls is DeviceClass.Mouse and hasattr(self, device.action):
                    action = getattr(self, device.action)
                    action(device)

    def add(self, device):
        self.devices.add(device)
        self.refresh()

    def remove(self, device):
        if device in self.devices:
            self.devices.remove(device)
        self.refresh()

    def refresh(self):
        if not self._touchpad:
            return

        if self.devices and not self._touchpad.toggled:
            self._touchpad.disable()
        else:
            self._touchpad.enable()

    def sig_handler(self, signum, frame):
        if signum == SIGTOGGLE:
            self._touchpad.toggle()
            self.refresh()
        else:
            sys.exit()
