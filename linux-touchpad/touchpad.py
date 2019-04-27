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

        out = subp.run(['xinput', 'list', self.name], capture_output=True)
        _, self.id = re.search(DEVICE_RE, out.stdout.decode()).groups()

    def disable(self):
        if not self.toggled:
            subp.run(['xinput', 'disable', self.id])

    def enable(self):
        subp.run(['xinput', 'enable', self.id])
