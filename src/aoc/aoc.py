from aoc.utils import get_day_data_directory
from pathlib import Path
import requests
import logging
import os

logger = logging.getLogger(__name__)

AOC_SESSION_FILE = Path('~/.aoc_session')

class Aoc:

    def __init__(self, token: str | None) -> None:

        if not token is None:
            self.token = token
            return
        else:
            logger.debug("No session token provided.")

        if AOC_SESSION_FILE.exists():
            with open(AOC_SESSION_FILE, 'r') as f:
                self.token = f.read().strip()
                return
        else:
            logger.debug("No session token found in ~/.aoc_session")

        if os.environ.get("AOC_SESSION"):
            self.token = os.environ["AOC_SESSION"]
            return
        else:
            logger.debug("No session token found in environment variables. (AOC_SESSION)")

        logger.error("No session token found. Please provide one.")
        raise ValueError("No session token found. Please provide one")


    def fetch_input(self, year: int, day: int) -> None:
        """Fetch the input data for the given year and day."""

        input_file = get_day_data_directory(year=year, day=day) / "input.txt"

        if input_file.exists():
            logger.info("Input data already fetched for year %s, day %s", year, day)
            return

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {"Cookie": f"session={self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        with open(input_file, "w") as f:
            f.write(response.text)

        logger.info("Input data fetched for year %s, day %s", year, day)

