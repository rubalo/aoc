from pathlib import Path
import git

git_repo = git.Repo(".", search_parent_directories=True)
git_root = git_repo.git.rev_parse("--show-toplevel")
ROOT_DIR = Path(git_root)

def create_day_structure(day: int, year: int) -> None:
    """Create the directory structure for the given day and year."""

    # Create the year directory

    # Create the day directory

    # Create the input file
    pass


def create_year_directory(year: int) -> None:
    """Create the year directory for the given year."""

    # Create the year directory
    year_dir = Path(f"{year}")
