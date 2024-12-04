from __future__ import annotations

import logging
from pathlib import Path

import git

from aoc.aoc import Aoc

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


def get_test_directory() -> Path:
    """Get the test directory for the Advent of Code solutions."""

    return get_root_directory() / Path("tests")


def get_year_directory(year: int) -> Path:
    """Get the year directory for the given year."""

    return get_module_directory() / Path(f"y{year}")


def get_year_test_directory(year: int) -> Path:
    """Get the year test directory for the given year."""

    return get_test_directory() / Path(f"y{year}")


def create_year_test_directory(year: int) -> None:
    """Create the year test directory for the given year."""

    year_dir = get_year_test_directory(year)
    create_module_structure(year_dir)


def get_year_data_directory(year: int) -> Path:
    """Get the year data directory for the given year."""

    return get_data_directory() / Path(f"y{year}")


def create_year_data_directory(year: int) -> None:
    """Create the year data directory for the given year."""

    year_dir = get_year_data_directory(year)
    create_data_structure(year_dir)


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


def create_test_structure(directory: Path) -> None:
    """Create the test structure for the Advent of Code solutions."""

    if directory.exists():
        logger.debug("Directory already exists: %s", directory)
    else:
        create_module_structure(directory)
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

    # Create the day file
    create_day_file(day, year)

    # Create the yeartest directory
    create_year_test_directory(year)

    # Create the day test file
    create_day_test_file(day, year)


def create_year_directory(year: int) -> None:
    """Create the year directory for the given year."""

    year_dir = get_module_directory() / Path(f"y{year}")
    create_module_structure(year_dir)


def create_day_file(day: int, year: int) -> None:
    """Create the day file for the given day and year from a template."""

    template = f"""# Advent of Code {year} - Day {day}

from __future__ import annotations
from aoc.utils import read_input

def get_input_data() -> list[str]:
    return read_input(day={day}, year={year})


def get_test_input_data() -> list[str]:
    return [""]


def part1() -> int:
    data = get_input_data()  # noqa
    return 0


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
"""

    day_file = get_year_directory(year) / Path(f"day{day:02}.py")

    if day_file.exists():
        _msg = f"Day file already exists: {day_file}, skipping..."
        logger.warning(_msg)
        return

    with open(day_file, "w") as f:
        f.write(template)

    logger.info("Created day file: %s", day_file)


def create_day_test_file(day: int, year: int) -> None:
    """Create the day test file for the given day and year from a template."""

    template = f"""# Advent of Code {year} - Day {day} - Test

from __future__ import annotations
from pathlib import Path

from aoc.y{year}.day{day:02} import part1, part2

def test_part1() -> None:
    assert part1() == 0

def test_part2() -> None:
    assert part2() == 0
"""

    day_test_file = get_year_test_directory(year) / Path(f"test_day{day:02}.py")

    if day_test_file.exists():
        _msg = f"Day test file already exists: {day_test_file}, skipping..."
        logger.warning(_msg)
        return

    with open(day_test_file, "w") as f:
        f.write(template)

    logger.info("Created day test file: %s", day_test_file)


def run_day(day: int, year: int, part: int) -> None:
    """Run the given day and year."""

    day_file = get_module_directory() / Path(f"y{year}/day{day:02}.py")

    if not day_file.exists():
        _msg = f"Day file does not exist: {day_file}"
        raise FileNotFoundError(_msg)

    # Import the day module
    from importlib import import_module

    module = import_module(f"aoc.y{year}.day{day:02}")

    logger.info("Day %d of year %d", day, year)
    # Run the solutions
    if part in (0, 1):
        part1 = module.part1()
        logger.info("Part 1: %s", part1)
    if part in (0, 2):
        part2 = module.part2()
        logger.info("Part 2: %s", part2)


def read_input(day: int, year: int) -> list[str]:
    """Read the input data for the given day and year."""

    day_file = get_data_directory() / Path(f"y{year}/day{day:02}_input.txt")

    if not day_file.exists():
        _msg = f"Day input file does not exist: {day_file}"
        try:
            aoc = Aoc(token=None)
            input_file = get_year_data_directory(year=year) / f"day{day:02}_input.txt"
            aoc.fetch_input(year, day, input_file)
        except Exception as e:
            raise FileNotFoundError(_msg) from e

    with open(day_file) as f:
        return f.readlines()
