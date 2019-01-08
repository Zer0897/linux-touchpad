import subprocess as subp
import signal
import asyncio as aio
import re

touchpad_id = '16'
mouse_name = 'Logitech M510'

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
    return re.findall(devicelist_re, rawout)


async def isenabled(device_id) -> bool:
    rawout = await run(['xinput', 'list-props', touchpad_id])
    return bool(re.search(enabled_re, rawout))


async def disable():
    subp.run(['xinput', 'disable', touchpad_id])


async def enable():
    subp.run(['xinput', 'enable', touchpad_id])


async def watchdevices():
    while running:
        touchpad_enabled: bool = await isenabled(touchpad_id)
        if toggled and not touchpad_enabled:
            await enable()
        elif not toggled:
            devices = await getdevices()
            names = (name for name, _ in devices)

            if mouse_name in names:
                if touchpad_enabled:
                    await disable()

            elif not touchpad_enabled:
                await enable()
        await aio.sleep(1)
