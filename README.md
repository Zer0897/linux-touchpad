# Linux Touchpad
----------------

A simple tool with one job: disable the touchpad on a laptop when a mouse is plugged in.

**Requires**

`Python >= 3.6`
```
python -V  # to check
```

[libinput](https://www.mankier.com/4/libinput) to manage the devices.


# Install
**Recommended**

The easiest way to get it is through the install script. This will add it to your `~/.local/bin` and configure it to run on startup.
```
curl -sSL https://raw.githubusercontent.com/Zer0897/linux-touchpad/master/install.py | python
```

*Alternatively*

It can be done through pip, but you won't get the config setup.
```
pip install linux-touchpad
```

## Uninstall
```
# Get the file
curl -sSL https://raw.githubusercontent.com/Zer0897/linux-touchpad/master/install.py > ~/Downloads/install.py
# Make it executable
chmod 777 ~/Downloads/install.py
# Run the uninstaller
python ~/Downloads/install.py --uninstall
```

## Installing Without Startup Behavior
Get the file as shown above, then run:
```
python ~/Downloads/install.py --no-autostart
```

# Usage

To begin:
```
linux-touchpad start&
```
Or if installed with pip:
```
python -m linux-touchpad start&
```
While running, this will toggle the touchpad on and off:
```
linux-touchpad toggle
```
*Tip: Set this command to a keyboard shortcut for maximum convenience*

Finally, to stop the process entirely:
```
linux-touchpad kill
```


### Author
Noah Corona | noah@coronsoftware.net
