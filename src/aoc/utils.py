import logging
from pathlib import Path

import git

MODULE_PATH = "src/aoc"

logger = logging.getLogger(__name__)


def get_root_directory() -> Path:
    """Get the root directory of the git repository."""

    git_repo = git.Repo(".", search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return Path(git_root)


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

def read_input() -> list[str]:
    file_path = Path(__file__) / "input.txt"
    with open(file_path, "r") as f:
        return f.readlines()

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
