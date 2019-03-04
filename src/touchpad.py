import subprocess as subp
import signal
import asyncio as aio
import re
import os

path = os.path.abspath(__file__)
path, _ = os.path.split(path)

touchpad_name = '1A582000:00 06CB:CD73 Touchpad'
with open(f'{path}/.mouse') as file:
    mouse_names = [l.strip('\n') for l in file]

devicelist_re = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')
enabled_re = re.compile(r'(?:Device Enabled.*\t)(1)')

SIGTOGGLE = signal.SIGUSR1

toggled: bool = False
running: bool = True


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


async def getdevices() -> dict:
    rawout = await run(['xinput', 'list'])
    return {name: id for name, id in re.findall(devicelist_re, rawout)}


async def getdeviceid(device_name) -> str:
    devices = await getdevices()
    return devices[device_name]


async def isenabled(device_id) -> bool:
    rawout = await run(['xinput', 'list-props', device_id])
    return bool(re.search(enabled_re, rawout))


async def disable(device_id):
    subp.run(['xinput', 'disable', device_id])


async def enable(device_id):
    subp.run(['xinput', 'enable', device_id])


async def watchdevices():
    touchpad_id = await getdeviceid(touchpad_name)
    while running:
        touchpad_enabled: bool = await isenabled(touchpad_id)
        if toggled and not touchpad_enabled:
            await enable(touchpad_id)
        elif not toggled:
            devices = await getdevices()
            found: bool = False
            for name in mouse_names:
                if name in devices:
                    found = True

            if found and touchpad_enabled:
                await disable(touchpad_id)

            elif not found and not touchpad_enabled:
                await enable(touchpad_id)
        await aio.sleep(1)
