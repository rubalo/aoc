# Advent of Code 2025 - Day 7

from __future__ import annotations

import logging
from typing import LiteralString, Tuple

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


def count_splits(data: list[list[str]]) -> Tuple[int, int]:
    beams_positions = set()
    nb_beams = [0] * len(data[0])

    # Get start position
    start_pos = data[0].index("S")
    nb_beams[start_pos] = 1
    beams_positions.add(start_pos)

    # Count splits
    splitter_count = 0
    timeline = 1

    logger.debug(f"Initial beam position at {start_pos}")
    logger.debug(f"Processing row : {data[0]}")
    for i, line in enumerate(data[1:]):
        logger.debug(f"Processing row : {line}")
        new_beans = set()
        for bean in beams_positions:
            if line[bean] == "^":
                new_beans.add(bean - 1)
                new_beans.add(bean + 1)
                logger.debug(f"Beam at {bean} split to {bean - 1} and {bean + 1}")
                splitter_count += 1
                timeline += nb_beams[bean]
                nb_beams[bean - 1] += nb_beams[bean]
                nb_beams[bean + 1] += nb_beams[bean]
                nb_beams[bean] = 0
            else:
                new_beans.add(bean)
        beams_positions = new_beans
        print(f"After row {i + 1}, nb_timelines={timeline}, beams at {beams_positions}")

    return splitter_count, timeline


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    print(data)
    nb_splitters, _ = count_splits(data)
    return nb_splitters


def part2() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    _, timelines = count_splits(data)
    return timelines
