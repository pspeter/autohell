# autohell

[![PyPI - Version](https://img.shields.io/pypi/v/autohell.svg)](https://pypi.org/project/autohell)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autohell.svg)](https://pypi.org/project/autohell)

-----

`autohell` controls your monitor's brightness ("hell" means bright in German) automatically.
For now, it keeps your monitor at 60% brightness during the day, and then slowly dims your
monitor starting at 7 PM and ends at 5% brightness at 9:30 PM. Why these values? Because I like
them. These values are currently not configurable. PR's welcome :)

If you change your monitors brightness at any time through any other means, autohell will stop
doing anything for 3 hours (or until you restart it).

## Installation

I recommend using [pipx](https://github.com/pypa/pipx) to install
Python executables:

```console
pipx install autohell
```

*Note*: `autohell` currently does not have any UI, if you run the executable from pipx, 
it will just run in the background. You have to use your task manager to stop it.

## License

`autohell` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
