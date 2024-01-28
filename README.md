# autohell

[![PyPI - Version](https://img.shields.io/pypi/v/autohell.svg)](https://pypi.org/project/autohell)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autohell.svg)](https://pypi.org/project/autohell)

-----

`autohell` controls your monitor's brightness ("hell" means bright in German) automatically.
For now, it keeps your monitor at 60% brightness during the day, and then slowly dims your
monitor starting at 7 PM and ends at 5% brightness at 9 PM. Why these values? Because I like them.
Yes, these values are currently not configurable. PR's welcome :)

## Installation

I recommend using [pipx](https://github.com/pypa/pipx) to install
Python executables:

```console
pipx install autohell
```

## License

`autohell` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
