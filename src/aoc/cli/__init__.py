# SPDX-FileCopyrightText: 2024-present rubalo <rubalo@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT
import logging
import sys
from datetime import UTC, datetime

import click

from aoc.__about__ import __version__
from aoc.aoc import Aoc
from aoc.utils import (
    create_day_structure,
    create_module_structure,
    create_year_data_directory,
    create_year_test_directory,
    get_data_directory,
    get_year_data_directory,
    get_year_test_directory,
    run_day,
)

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
@click.option("--token", "-t", help="Session token for the Advent of Code", required=False)
@click.version_option(version=__version__, prog_name="aoc")
@click.pass_context
def aoc(ctx, *, verbose: bool, day: int, year: int, token: str) -> None:
    click.echo("Advent of code!")

    ctx.ensure_object(dict)

    c_year = datetime.now(UTC).year
    c_day = datetime.now(UTC).day

    ctx.obj["verbose"] = verbose
    ctx.obj["token"] = token

    if verbose:
        r_logger = logging.getLogger("root")
        r_logger.setLevel(logging.DEBUG)
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

    # init data directory
    data_dir = get_data_directory()
    if not data_dir.exists():
        create_module_structure(data_dir)


@aoc.command()
@click.pass_context
def init(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]

    _init_day(day, year)


@aoc.command()
@click.pass_context
def run(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]

    _run_day(day, year)


@aoc.command()
@click.pass_context
def fetch_day(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]
    token = ctx.obj["token"]

    _fetch_day(day, year, token)


@aoc.command(help="Initialize, fetch and run the given day and year.")
@click.pass_context
def day(ctx) -> None:
    day = ctx.obj["day"]
    year = ctx.obj["year"]
    token = ctx.obj["token"]

    _init_day(day, year)
    _fetch_day(day, year, token)
    _run_day(day, year)


def _init_day(day: int, year: int) -> None:
    """Initialize the given day and year."""

    _msg = f"Initializing day {day} of year {year}"
    logger.info(_msg)

    # Create the directory structure
    try:
        create_day_structure(day, year)
    except FileExistsError:
        logger.exception("Day file already exists.")
        logger.info("Aborting...")
        sys.exit(1)

    _msg = f"Day {day} of year {year} initialized."
    logger.info(_msg)


def _run_day(day: int, year: int) -> None:
    """Run the given day and year."""

    _msg = f"Running day {day} of year {year}"
    logger.info(_msg)

    try:
        run_day(day, year)
    except FileNotFoundError:
        logger.exception("Day file does not exist.")
        logger.info("Aborting...")
        sys.exit(1)

    _msg = f"Day {day} of year {year} run."


def _fetch_day(day: int, year: int, token: str) -> None:
    """Fetch the input data for the given day and year."""

    _msg = f"Fetching input for day {day} of year {year}"
    logger.info(_msg)

    if not get_year_data_directory(year).exists():
        create_year_data_directory(year)

    if not get_year_test_directory(year).exists():
        create_year_test_directory(year)

    try:
        aoc = Aoc(token)
        aoc.fetch_input(year, day)
    except ValueError:
        logger.exception("No session token found.")
        logger.info("Aborting...")
        sys.exit(1)
