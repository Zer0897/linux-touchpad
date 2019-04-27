import re
import signal
import subprocess as subp

SIGTOGGLE = signal.SIGUSR1
DEVICE_RE = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')


class TouchPad:
    toggled = False

    def __init__(self, device):
        self.device = device
        self.name = self.device.parent.attributes.get('name').decode()

    def disable(self):
        print('disabled')
        if not self.toggled:
            subp.run(['xinput', 'disable', self.name])

    def enable(self):
        print('enabled')
        subp.run(['xinput', 'enable', self.name])
