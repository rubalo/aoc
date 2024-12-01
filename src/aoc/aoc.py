from __future__ import annotations

import logging
import os
from pathlib import Path

import requests

from aoc.utils import get_year_data_directory

logger = logging.getLogger(__name__)

AOC_SESSION_FILE = Path("~/.aoc_session").expanduser()


class Aoc:
    def __init__(self, token: str | None) -> None:
        if token is not None:
            self.token = token
            return
        logger.debug("No session token provided.")

        if AOC_SESSION_FILE.is_file():
            with open(AOC_SESSION_FILE) as f:
                self.token = f.read().strip()
                return
        logger.debug("No session token found in ~/.aoc_session")

        if os.environ.get("AOC_SESSION"):
            self.token = os.environ["AOC_SESSION"]
            return
        logger.debug("No session token found in environment variables. (AOC_SESSION)")

        logger.error("No session token found. Please provide one.")
        raise ValueError

    def fetch_input(self, year: int, day: int) -> None:
        """Fetch the input data for the given year and day."""

        input_file = get_year_data_directory(year=year) / f"day{day}_input.txt"

        if input_file.exists():
            logger.info("Input data already fetched for year %s, day %s", year, day)
            return

        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {"Cookie": f"session={self.token}"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()

        with open(input_file, "w") as f:
            f.write(response.text)

        logger.info("Input data fetched for year %s, day %s", year, day)
