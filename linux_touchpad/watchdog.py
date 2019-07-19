from pyudev import Context, Monitor, Device
from .touchpad import TouchPad


# The properties that usb mice probably have in common
MOUSE_PROPS = {
    'removable': 'removable',
    # 'phys': 'usb',
    'name': 'mouse'
}



def is_mouse(device: Device) -> bool:
    """
    Return True if the device looks like a mouse. This is necessary
    to filter out controllers that get caught in the pudev mouse query.

    Args:
        device : Device
            The device in question.

    Returns: bool
    """
    props = set(MOUSE_PROPS.values())
    found = set()
    for dev in (device, *device.ancestors):
        if found == props:
            break

        for name, val in MOUSE_PROPS.items():
            prop = dev.attributes.get(name)
            if prop and val in prop.decode().casefold():
                found.add(val)

    is_pci = device.find_parent('pci')
    matched = set(MOUSE_PROPS.values()) & found
    return bool(matched) or not is_pci


class WatchDog:
    """The sentry for input device based events."""
    context = Context()
    touchpad_toggled = False


    def __init__(self):
        self._mice = set()
        self._touchpads = set()

        self.monitor = Monitor.from_netlink(self.context)
        self.monitor.filter_by('input')

    def __refresh_devices(self):
        touchpads = self.context.list_devices(subsystem='input', sys_name='mouse*', ID_INPUT_TOUCHPAD=True)
        devices = self.context.list_devices(subsystem='input', sys_name='mouse*', ID_INPUT_MOUSE=True)

        self._touchpads = {TouchPad(dev) for dev in touchpads}
        self._mice = {dev for dev in devices if is_mouse(dev)}

    def __on_device(self, device):
        if device.action == 'add':
            self._mice.add(device)
        elif device.action == 'remove':
            self._mice.remove(device)

        self.__update_touchpad()

    def __update_touchpad(self):
        action = 'disable' if self._mice and not self.touchpad_toggled else 'enable'
        for touchpad in self._touchpads:
            getattr(touchpad, action)()

    def start(self):
        """Begin watching for devices"""
        self.__refresh_devices()
        self.__update_touchpad()
        for device in iter(self.monitor.poll, None):
            valid: bool = all((
                'mouse' in device.sys_name,
                device.action in ('add', 'remove'),
                is_mouse(device)
            ))
            if valid:
                self.__on_device(device)

    def toggle_touchpad(self, *_):
        self.touchpad_toggled = not self.touchpad_toggled
        self.__update_touchpad()
