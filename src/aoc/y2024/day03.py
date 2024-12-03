# Advent of Code 2024 - Day 3

from __future__ import annotations

import re

from aoc.utils import read_input


def get_input_data() -> list[str]:
    return read_input(day=3, year=2024)


def get_test_input_data() -> list[str]:
    return [""]


def part1() -> int:
    data = get_input_data()

    parser = re.compile(r"mul\((\d+),(\d+)\)")
    res = 0

    for line in data:
        match = parser.findall(line)
        for x, y in match:
            res += int(x) * int(y)
    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
