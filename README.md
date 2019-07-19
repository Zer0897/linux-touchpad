A simple, lightweight command line utility for managing your touchpad.

-   Disable when a mouse is detected.
-   Enabled when no mice are detected.
-   Toggle this behavior.

For a more feature-rich implementation, see [touchpad-indicator](https://launchpad.net/touchpad-indicator).


# Dependencies

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Python 3.7</td>
<td class="org-left">https://www.python.org/downloads/release/python-373/</td>
</tr>


<tr>
<td class="org-left">Libinput</td>
<td class="org-left">https://wiki.archlinux.org/index.php/Libinput</td>
</tr>
</tbody>
</table>


# Install

    $ pip install linux-touchpad


# Usage


## Start

To begin the process, use this command:

    $ python -m linux_touchpad start


## Toggle

Enabled the touchpad and ignore mouse events:

    $ python -m linux_touchpad toggle


## Stop

    $ python -m linux_touchpad stop


# Author

[Noah Corona](https://github.com/Zer0897)
[noah@coronasoftware.net](mailto:noah@coronasoftware.net)

[![img](https://coronasoftware.net/s/sLogo.png)](https://coronasoftware.net)
