from enum import Enum
from collections import defaultdict


class DeviceClass(Enum):
    TouchPad = 0
    Mouse = 1
    Other = 2


def identify(device) -> DeviceClass:
    props = look(device, 'removable', 'phys')

    def find_in(it, name):
        return any(name in item.casefold() for item in it)

    if 'removable' in props['removable']:
        return DeviceClass.Mouse

    # USB but not removable probably means it's a controller
    if find_in(props['phys'], 'usb'):
        return DeviceClass.Other

    return DeviceClass.TouchPad


def look(device, *names) -> dict:
    data = defaultdict(list)
    for dev in [device] + list(device.ancestors):
        for name in names:
            prop = dev.attributes.get(name)
            if prop is not None:
                data[name].append(prop.decode())

    return data
