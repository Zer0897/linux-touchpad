import subprocess as subp
import asyncio as aio
import re

touchpad_id = '16'
mouse_name = 'Logitech M510'

devicelist_re = re.compile(r'(\w.+\b(?=\W.+id))(?:.+id=)(\d+)')
enabled_re = re.compile(r'(?:Device Enabled.*\t)(1)')


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


async def watchdevices():
    while True:
        devices = await getdevices()
        names = (name for name, _ in devices)
        touchpad_enabled: bool = await isenabled(touchpad_id)
        if mouse_name in names:
            if touchpad_enabled:
                subp.run(['xinput', 'disable', touchpad_id])
        elif not touchpad_enabled:
            subp.run(['xinput', 'enable', touchpad_id])

        await aio.sleep(1)


aio.run(watchdevices())
