# SPDX-FileCopyrightText: 2024-present rubalo <rubalo@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import click
from datetime import datetime

from aoc.__about__ import __version__
from aoc.utils import create_day_structure


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.version_option(version=__version__, prog_name="aoc")
def aoc():
    click.echo("Advent of code!")


@aoc.command()
@click.option("--day", "-d", type=int, help="Day of the Advent of Code", default=datetime.now().day)
@click.option("--year", "-y", type=int, help="Year of the Advent of Code", default=datetime.now().year)
def init(day: int, year: int) -> None:
    click.echo(f"Initializing day {day} of year {year}")

    # Create the directory structure
    create_day_structure(day, year)

