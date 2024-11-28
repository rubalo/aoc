from __future__ import annotations

import logging
from datetime import UTC, datetime
from pathlib import Path

import git

MODULE_PATH = "src/aoc"

logger = logging.getLogger(__name__)


def get_root_directory() -> Path:
    """Get the root directory of the git repository."""

    git_repo = git.Repo(".", search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return Path(git_root)


def get_data_directory() -> Path:
    """Get the data directory for the Advent of Code solutions."""

    return get_root_directory() / Path("data")


def get_day_data_directory(day: int, year: int = 0) -> Path:
    """Get the day data directory for the given day and year."""

    if year == 0:
        year = datetime.now(UTC).year

    return get_data_directory() / Path(f"{year}/day{day}")


def get_year_data_directory(year: int) -> Path:
    """Get the year data directory for the given year."""

    return get_data_directory() / Path(f"{year}")


def create_year_data_directory(year: int) -> None:
    """Create the year data directory for the given year."""

    year_dir = get_year_data_directory(year)
    create_data_structure(year_dir)


def create_day_data_directory(day: int, year: int) -> None:
    """Create the day data directory for the given day and year."""

    day_dir = get_day_data_directory(day, year)
    create_data_structure(day_dir)


def get_module_directory() -> Path:
    """Get the module directory for the Advent of Code solutions."""

    return get_root_directory() / Path(MODULE_PATH)


def create_module_structure(directory: Path) -> None:
    """Create the module structure for the Advent of Code solutions."""

    if directory.exists():
        logger.debug("Directory already exists: %s", directory)
    else:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info("Created directory: %s", directory)

    if not (directory / Path("__init__.py")).exists():
        with open(directory / Path("__init__.py"), "w") as f:
            f.write("")
        logger.info("Created __init__.py file:  %s", directory / Path("__init__.py"))


def create_data_structure(directory: Path) -> None:
    """Create the data structure for the Advent of Code solutions."""

    if directory.exists():
        logger.debug("Directory already exists: %s", directory)
    else:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info("Created directory: %s", directory)


def create_module_directory() -> None:
    """Create the module directory for the Advent of Code solutions."""

    module_dir = get_module_directory()
    create_module_structure(module_dir)


def create_day_structure(day: int, year: int) -> None:
    """Create the directory structure for the given day and year."""

    # Check base module directory exists
    module_dir = get_module_directory()
    if not module_dir.exists():
        create_module_directory()

    # Create the year directory
    create_year_directory(year)

    # Create the day directory
    create_day_directory(day, year)

    # Create the day file
    create_day_file(day, year)


def create_year_directory(year: int) -> None:
    """Create the year directory for the given year."""

    year_dir = get_module_directory() / Path(f"{year}")
    create_module_structure(year_dir)


def create_day_directory(day: int, year: int) -> None:
    """Create the day directory for the given day and year."""

    day_dir = get_module_directory() / Path(f"{year}/day{day}")
    create_module_structure(day_dir)


def create_day_file(day: int, year: int) -> None:
    """Create the day file for the given day and year from a template."""

    template = f"""# Advent of Code {year} - Day {day}

from __future__ import annotations
from pathlib import Path
from aoc.utils import read_input

def get_input_data() -> list[str]:
    return read_input(day={day}, year={year})


def get_test_input_data() -> list[str]:
    return [""]


def part1(data: list[str]) -> int:  # noqa
    return 0

def part2(data: list[str]) -> int:  # noqa
    return 0

"""

    day_file = get_module_directory() / Path(f"{year}/day{day}/day{day}.py")

    if day_file.exists():
        _msg = f"Day file already exists: {day_file}"
        raise FileExistsError(_msg)

    with open(day_file, "w") as f:
        f.write(template)

    logger.info("Created day file: %s", day_file)


def run_day(day: int, year: int) -> None:
    """Run the given day and year."""

    day_file = get_module_directory() / Path(f"{year}/day{day}/day{day}.py")

    if not day_file.exists():
        _msg = f"Day file does not exist: {day_file}"
        raise FileNotFoundError(_msg)

    # Import the day module
    from importlib import import_module

    module = import_module(f"aoc.{year}.day{day}.day{day}")

    # Read the input
    data = read_input(day, year)

    # Run the solutions
    part1 = module.part1(data)
    part2 = module.part2(data)

    logger.info("Day %d of year %d", day, year)
    logger.info("Part 1: %s", part1)
    logger.info("Part 2: %s", part2)


def read_input(day: int, year: int) -> list[str]:
    """Read the input data for the given day and year."""

    day_file = get_data_directory() / Path(f"{year}/day{day}/input.txt")

    if not day_file.exists():
        _msg = f"Day input file does not exist: {day_file}"
        raise FileNotFoundError(_msg)

    with open(day_file) as f:
        return f.readlines()
