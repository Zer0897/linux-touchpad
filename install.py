import sys
import subprocess as subp
from pathlib import Path
from argparse import ArgumentParser


NAME = 'linux-touchpad'
HOME = Path.home()
AUTOSTART = HOME / '.config' / 'autostart'
BIN = HOME / '.local' / 'bin'

COMMAND_FP = BIN / NAME
DESKTOP_APP_FP = (AUTOSTART / NAME).with_suffix('.desktop')


def install(no_autostart=False):
    print('Downloading package...')
    subp.run([sys.executable, '-m', 'pip', 'install', '--upgrade', NAME])
    print('Ok.')

    print('Installing...')
    COMMAND_FP.write_text(f"{sys.executable} -m linux-touchpad $1\n")
    COMMAND_FP.chmod(500)
    print('Ok.')

    if no_autostart:
        return

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
    TryExec={COMMAND_FP}
    Exec={COMMAND_FP} start
    StartupNotify=true
    X-GNOME-Autostart-enabled=false

    """
    DESKTOP_APP_FP.write_text(desktop_app)
    print('Ok.')


def uninstall():
    print('Uninstalling...')
    subp.run([sys.executable, '-m', 'pip', 'uninstall', NAME])
    for fp in (COMMAND_FP, DESKTOP_APP_FP):
        if fp.exists():
            fp.unlink()


def main():
    parser = ArgumentParser()
    parser.add_argument(
        '--no-autostart', '-n',
        action='store_true',
        help="Do not auto run on system startup.",
    )
    parser.add_argument(
        '--uninstall', '-u',
        action='store_true',
        help=f"Remove {NAME} from your system."
    )
    args = parser.parse_args()
    if args.uninstall:
        uninstall()
    else:
        install(args.no_autostart)


if __name__ == '__main__':
    main()
