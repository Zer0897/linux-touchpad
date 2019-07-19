import re
import signal
import subprocess as subp

SIGTOGGLE = signal.SIGUSR1


class TouchPad:
    enabled_re = re.compile(r'Device Enabled.*: *1')

    def __init__(self, device):
        self.device = device
        self.name = self.device.parent.attributes.get('name').decode()

    def disable(self):
        subp.run(['xinput', 'disable', self.name])

    def enable(self):
        subp.run(['xinput', 'enable', self.name])

    @property
    def enabled(self):
        result = subp.run(['xinput', '--list-props', self.name], capture_output=True)
        text = result.stdout.decode()
        return bool(self.enabled_re.search(text))
