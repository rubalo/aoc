# SPDX-FileCopyrightText: 2024-present rubalo <rubalo@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import click

from aoc.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="aoc")
def aoc():
    click.echo("Hello world!")
