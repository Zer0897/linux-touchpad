import sys
from enum import Enum
from pyudev import Context, Monitor, Device
from contextlib import suppress
from typing import Tuple, Set
from .touchpad import TouchPad, SIGTOGGLE


class DeviceType(Enum):
    TouchPad = 0
    USB = 1
    OTHER = 2


def identify(device: Device) -> DeviceType:

    def look(*items: Tuple[str, str]) -> Set['str']:
        found = set()
        for dev in [device] + list(device.ancestors):
            for name, val in items:
                prop = dev.attributes.get(name)
                if prop and val in prop.decode().casefold():
                    found.add(val)
        return found

    props = look(
        ('removable', 'removable'),
        ('phys', 'usb'),
        ('name', 'mouse'),
    )

    is_pci = device.find_parent('pci')
    if {'removable', 'mouse'} & props or not is_pci:
        return DeviceType.USB

    # USB but not removable probably means it's a controller
    if 'usb' in props:
        return DeviceType.OTHER

    return DeviceType.TouchPad


class WatchDog:
    context = Context()

    _devices = set()
    _touchpad: TouchPad = None

    def __init__(self):
        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by('input')

        for dev in self.context.list_devices(subsystem='input', sys_name='mouse*'):
            cls = identify(dev)

            if cls is DeviceType.TouchPad:
                if self._touchpad is None:
                    self._touchpad = TouchPad(dev)
                else:
                    raise ValueError('Found multiple TouchPads.')

            elif cls is DeviceType.USB:
                self._devices.add(dev)

        self.update()

    def __on_device(self, device):
        action = getattr(self._devices, device.action)  # self._devices.add or self._devices.remove
        with suppress(KeyError):
            action(device)
        self.update()

    def start(self):
        for device in iter(self.monitor.poll, None):
            valid: bool = all((
                'mouse' in device.sys_name,
                device.action in ('add', 'remove'),
                identify(device) is DeviceType.USB
            ))
            if valid:
                self.__on_device(device)

    def update(self):
        if self._devices and not self._touchpad.toggled:
            self._touchpad.disable()
        else:
            self._touchpad.enable()

    def sig_handler(self, signum, frame):
        if signum == SIGTOGGLE:
            self._touchpad.toggle()
            self.update()
        else:
            sys.exit()
