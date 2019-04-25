import re
import subprocess as subp
import signal
import asyncio as aio

from operator import itemgetter
from typing import Coroutine


SIGTOGGLE = signal.SIGUSR1
DEVICE_RE = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')
ENABLED_RE = re.compile(r'(?:Device Enabled.*\t)(1)')


toggled = False
running = True


def toggle():
    global toggled
    toggled = not toggled


def kill():
    global running
    running = False


async def run(command: list) -> str:
    ps = await aio.create_subprocess_exec(*command, stdout=subp.PIPE)
    raw = await ps.stdout.read()
    return raw.decode()


async def get_devices() -> dict:
    rawout = await run(['xinput', 'list'])
    out = re.findall(DEVICE_RE, rawout)
    props = await aio.gather(*(parse_props(name, id) for name, id in out))
    mice = filter(itemgetter('is_mouse'), props)

    return {mouse.pop('name'): mouse for mouse in mice}


async def parse_props(device: str, device_id: str) -> bool:
    rawout = await run(['xinput', 'list-props', device_id])

    props = {
        'name': device if 'touchpad' not in device.casefold() else 'touchpad',
        'id': device_id,
        'is_enabled': bool(re.search(ENABLED_RE, rawout)),
        'is_mouse': bool(re.search('Accel Speed', rawout)),
    }
    return props


async def disable_device(device_id):
    await run(['xinput', 'disable', device_id])


async def enable_device(device_id):
    await run(['xinput', 'enable', device_id])


async def get_action() -> Coroutine:
    global toggled

    devices = await get_devices()
    touchpad = devices.pop('touchpad')
    mouse_exists = len(devices) > 1
    touchpad_enabled = touchpad['is_enabled']
    touchpad_id = touchpad['id']

    if (toggled or not mouse_exists) and not touchpad_enabled:
        return enable_device(touchpad_id)
    elif mouse_exists and touchpad_enabled and not toggled:
        return disable_device(touchpad_id)
    else:
        return aio.sleep(0)


async def watch_devices():
    global running

    while running:
        action = await get_action()
        await aio.gather(action, aio.sleep(1))
