import subprocess as subp
import signal
import asyncio as aio
import aiofiles
import re
from pathlib import Path
from typing import Coroutine
from aiostream import stream


MOUSE_FP = Path(__file__).with_name('.mouse')
SIGTOGGLE = signal.SIGUSR1
DEVICE_RE = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')
ENABLED_RE = re.compile(r'(?:Device Enabled.*\t)(1)')

touchpad_name = None
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


async def get_touchpad_id(devices: dict) -> str:
    global touchpad_name
    if touchpad_name is None:
        async for name in stream.iterate(devices):
            await aio.sleep(0)
            if 'touchpad' in name.casefold():
                touchpad_name = name

    return devices[touchpad_name]


async def get_devices() -> dict:
    rawout = await run(['xinput', 'list'])
    return {name: id for name, id in re.findall(DEVICE_RE, rawout)}


async def get_mouse_names() -> list:
    names = set()
    async with aiofiles.open(str(MOUSE_FP)) as fp:
        async for name in fp:
            names.add(name.rstrip('\n'))
    return names


async def is_enabled(device_id) -> bool:
    rawout = await run(['xinput', 'list-props', device_id])
    return bool(re.search(ENABLED_RE, rawout))


async def check_for_mouse(devices) -> bool:
    names = await get_mouse_names()
    return names & set(devices)


async def disable_device(device_id):
    await run(['xinput', 'disable', device_id])


async def enable_device(device_id):
    await run(['xinput', 'enable', device_id])


async def get_action() -> Coroutine:
    global toggled

    devices = await get_devices()
    touchpad_id, mouse_exists = await aio.gather(
        get_touchpad_id(devices), check_for_mouse(devices)
    )
    touchpad_enabled = await is_enabled(touchpad_id)

    if (toggled or not mouse_exists) and not touchpad_enabled:
        return enable_device(touchpad_id)
    elif mouse_exists and touchpad_enabled and not toggled:
        return disable_device(touchpad_id)

    return aio.sleep(0)


async def watch_devices():
    global running

    while running:
        action = await get_action()
        await aio.gather(action, aio.sleep(1))
