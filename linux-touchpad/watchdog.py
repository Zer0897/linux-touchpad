from pyudev import Context, Monitor

from .touchpad import TouchPad
from .device import DeviceClass, identify


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
                    action()

    def add(self, device):
        self.devices.add(device)

    def remove(self, device):
        if device.sys_name in self.devices:
            del self.devices[device.sys_name]

    def refresh(self):
        if self.devices:
            self._touchpad.enable()
        else:
            self._touchpad.disable()
