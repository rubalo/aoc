# aoc

[![PyPI - Version](https://img.shields.io/pypi/v/aoc.svg)](https://pypi.org/project/aoc)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aoc.svg)](https://pypi.org/project/aoc)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Requirements

- Python 3.12 or higher
- uv [Astral](https://docs.astral.sh/uv/)

## Configuration

Update Aoc session cookie in `~/.aoc_session`. The session cookie
can be found in your browser cookies when logged into [Advent of Code](https://adventofcode.com/).

You can also pass it as an environment variable.

```console
export AOC_SESSION="your_session_cookie_here"
```

## Installation

```console
uv sync
uv run aoc
```

Run a specific day:

```console
uv run aoc --day 5 --year 2025 run [--part 1]
```

Run pre-commit checks:

```console
uv run pre-commit
```

Run tests:

```console
uv run pytest tests/y2025
```

## License

`aoc` is distributed under the terms of the
[MIT](https://spdx.org/licenses/MIT.html) license.
