# FooLaunchy
Python plugin for controlling foobar2000 through Launchy.

## Requirements
 - [foobar2000](https://www.foobar2000.org)
 - [foobar2000 beefweb web interface plugin](https://github.com/hyperblast/beefweb)
 - [Launchy](https://www.launchy.net/)
 - [Launchy PyLaunchy plugin](https://pylaunchy.sourceforge.io/docs/) (requires [Python 2.7 32bit](https://www.python.org))

## Installation
 - Put `foolaunchy.py` into `[launchy_install_dir]/plugins/python` directory.
 - Put `foobar2000_64.png` into `[launchy_install_dir]/plugins/icons` directory.
 - Restart Launchy.

## Usage
Type `foo [command]` into Launchy, where recognized commands are:
 - *play*, *pl* or *y* for **play**,
 - *stop* or *s* for **stop**,
 - *pause* or *p* for **pause** and **unpause**,
 - *next* or *n* for **next**,
 - *previous*, *prev* or *pr* for **previous**,
 - *volume up*, *vup* or *vu* for **increasing volume by 2dB**,
 - *volume down*, *vdn* or *vd* for **decreasing volume by 2dB** and
 - *mute* or *m* for **muting** and **unmuting**.

## Additional Notes
*FooLaunchy* plugin controls *foobar2000* by sending HTTP requests to [beefweb ReST API](https://hyperblast.org/beefweb/api/).
It assumes, that beefweb ReST services are running on **localhost** and on their default port **8880**.
If either hostname, port or both should be different, variables `BEEFWEB_HOST` and/or `BEEFWEB_PORT` should be emended accordingly in the `foolaunchy.py` script that is inside `[launchy_install_dir]/plugins/python` directory.
