import subprocess as subp
import signal
import asyncio as aio
import aiofiles
import re
from pathlib import Path
from typing import Coroutine


MOUSE_FP = Path(__file__).with_name('.mouse')
SIGTOGGLE = signal.SIGUSR1
DEVICE_RE = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')
ENABLED_RE = re.compile(r'(?:Device Enabled.*\t)(1)')

touchpad_name = '1A582000:00 06CB:CD73 Touchpad'
toggled = False
running = True


def toggle():
    global toggled
    toggled = not toggled


def kill():
    global running
    running = False


async def run(command):
    ps = await aio.create_subprocess_exec(*command, stdout=subp.PIPE)
    raw = await ps.stdout.read()
    return raw.decode()


async def get_devices() -> dict:
    rawout = await run(['xinput', 'list'])
    return {name: id for name, id in re.findall(DEVICE_RE, rawout)}


async def get_mouse_names() -> list:
    async with aiofiles.open(str(MOUSE_FP)) as fp:
        return set(l.strip('\n') async for l in fp)


async def is_enabled(device_id) -> bool:
    rawout = await run(['xinput', 'list-props', device_id])
    return bool(re.search(ENABLED_RE, rawout))


async def disable_device(device_id):
    await run(['xinput', 'disable', device_id])


async def enable_device(device_id):
    await run(['xinput', 'enable', device_id])


async def get_action() -> Coroutine:
    global touchpad_name
    global toggled

    mouse_names, all_devices = await aio.gather(
        get_mouse_names(), get_devices()
    )
    touchpad_id = all_devices[touchpad_name]
    mouse_exists = bool(set(all_devices) & mouse_names)
    touchpad_enabled = await is_enabled(touchpad_id)

    if (toggled or not mouse_exists) and not touchpad_enabled:
        return enable_device(touchpad_id)
    elif mouse_exists and touchpad_enabled and not toggled:
        return disable_device(touchpad_id)

    return aio.sleep(0)


async def watch_devices():
    global running

    action = await get_action()
    while running:
        action, _ = aio.gather(get_action(), action)
