import signal
import subprocess as subp

SIGTOGGLE = signal.SIGUSR1


class TouchPad:

    def __init__(self, device):
        self.device = device
        self.name = self.device.parent.attributes.get('name').decode()

    def disable(self):
        subp.run(['xinput', 'disable', self.name])

    def enable(self):
        subp.run(['xinput', 'enable', self.name])
