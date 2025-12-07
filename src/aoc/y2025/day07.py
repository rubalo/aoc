# Advent of Code 2025 - Day 7

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


def get_input_data():
    return read_input(day=7, year=2025)


def parse_data(data: list[str]):
    input = []
    for line in data:
        if not line.strip():
            continue
        input.append([x for x in line.strip()])
    return input


def get_test_input_data() -> list[LiteralString]:
    data = """
    .......S.......
    ...............
    .......^.......
    ...............
    ......^.^......
    ...............
    .....^.^.^.....
    ...............
    ....^.^...^....
    ...............
    ...^.^...^.^...
    ...............
    ..^...^.....^..
    ...............
    .^.^.^.^.^...^.
    ...............
"""
    return data.split("\n")


def count_splits(data: list[list[str]]) -> int:
    beams_positions = set()

    # Get start position
    start_pos = data[0].index("S")
    beams_positions.add(start_pos)

    # Count splits
    splitter_count = 0

    logger.debug(f"Initial beam position at {start_pos}")
    logger.debug(f"Processing row : {data[0]}")
    for line in data[1:]:
        logger.debug(f"Processing row : {line}")
        new_beans = set()
        for bean in beams_positions:
            if line[bean] == "^":
                new_beans.add(bean - 1)
                new_beans.add(bean + 1)
                logger.debug(f"Beam at {bean} split to {bean - 1} and {bean + 1}")
                splitter_count += 1
            else:
                new_beans.add(bean)
        beams_positions = new_beans

    return splitter_count


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    print(data)
    result = count_splits(data)
    print(f"Number of splitters passed: {result}")
    return result


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
