# SPDX-FileCopyrightText: 2024-present rubalo <rubalo@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import logging
from datetime import UTC, datetime

import click

from aoc.__about__ import __version__
from aoc.utils import create_day_structure, run_day

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)
logger = logging.getLogger(__name__)

MIN_AOC_YEAR = 2015


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=False)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option("--day", "-d", type=int, help="Day of the Advent of Code", required=False, default=0)
@click.option("--year", "-y", type=int, help="Year of the Advent of Code", required=False, default=0)
@click.version_option(version=__version__, prog_name="aoc")
@click.pass_context
def aoc(ctx, *, verbose: bool, day: int, year: int) -> None:
    click.echo("Advent of code!")

    ctx.ensure_object(dict)

    c_year = datetime.now(UTC).year
    c_day = datetime.now(UTC).day

    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled.")

    if year == 0:
        i_year = click.prompt("Enter the year of the Advent of Code", type=int, default=c_year)
        if not MIN_AOC_YEAR < i_year < c_year + 1:
            click.echo(f"Year must be between 2015 and {c_year}")
            click.echo("Aborting...")
            return
        ctx.obj["year"] = i_year
    else:
        ctx.obj["year"] = year

    if day == 0:
        # Ask user if he wants to use the current day
        i_day = click.prompt("Enter the day", type=int, default=c_day)

        if not 0 < i_day < 31 + 1:
            click.echo("Day must be between 1 and 31")
            click.echo("Aborting...")
            return
        ctx.obj["day"] = i_day
    else:
        ctx.obj["day"] = day


@aoc.command()
@click.pass_context
def init(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]

    _msg = f"Initializing day {day} of year {year}"
    logger.info(_msg)

    # Create the directory structure
    try:
        create_day_structure(day, year)
    except FileExistsError:
        logger.exception("Day file already exists.")
        logger.info("Aborting...")
        return

    _msg = f"Day {day} of year {year} initialized."
    logger.info(_msg)


@aoc.command()
@click.pass_context
def run(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]

    _msg = f"Running day {day} of year {year}"
    logger.info(_msg)

    try:
        run_day(day, year)
    except FileNotFoundError:
        logger.exception("Day file does not exist.")
        logger.info("Aborting...")
        return

    _msg = f"Day {day} of year {year} run."

