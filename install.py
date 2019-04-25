import sys
import subprocess as subp
from pathlib import Path

NAME = 'linux-touchpad'
HOME = Path.home()
AUTOSTART = HOME / '.config' / 'autostart'
BIN = HOME / '.local' / 'bin'


print('Downloading package...')
subp.run([sys.executable, '-m', 'pip', 'install', NAME])
print('Ok.')


print('Installing...')
command_fp = BIN / NAME
command_fp.write_text(f"{sys.executable} -m linux-touchpad\n")
print('Ok.')


autostart = input('Run on startup? ([y]/n): ')
if 'n' in autostart.casefold():
    sys.exit()

print('Setting up autostart...')
desktop_app = f"""\
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Application
Name={NAME}
Comment=Auto disable touchpad when mouse detected.
Keywords=mouse;touchpad;auto;detect;
Categories=Settings;System;
TryExec={command_fp}
Exec={command_fp} start
StartupNotify=true
X-GNOME-Autostart-enabled=false

"""
desktop_app_fp = (AUTOSTART / NAME).with_suffix('.desktop')
desktop_app_fp.write_text(desktop_app)
print('Ok.')
