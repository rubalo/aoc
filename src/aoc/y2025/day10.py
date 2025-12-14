# Advent of Code 2025 - Day 10

from __future__ import annotations

import logging
import re
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


# Parser for a machine like:
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
re_pattern = re.compile(
    r"^(?P<diagram>\[([.#]+)\])\s"
    r"(?P<buttons>(?:\(\s*[^)]*\s*\)\s*)+)\s"
    r"(?P<joltages>\{([0-9]+(,[0-9]+)*)\})$"
)


class Machine:
    diagram: list[str]
    buttons: list[tuple]
    joltages: set[int]

    def __init__(self, line: str):
        self.parse_input(line)

    def parse_input(self, line: str):
        logger.debug(f"Parsing line: {line}")

        match = re_pattern.match(line.strip())

        if not match:
            raise ValueError(f"Line does not match pattern: {line}")
        diagram_str = match.group("diagram")
        buttons_str = match.group("buttons")
        joltages_str = match.group("joltages")
        self.diagram = list(diagram_str[1:-1])
        self.buttons = [
            tuple(int(num) for num in btn.strip("()").split(","))
            for btn in buttons_str.strip().split()
        ]
        self.joltages = set(
            int(jolt.strip()) for jolt in joltages_str.strip("{}").split(",")
        )

    def __str__(self):
        return f"Machine(diagram={self.diagram}, buttons={self.buttons}, joltages={self.joltages})"


def get_input_data():
    return read_input(day=10, year=2025)


def parse_data(data: list[str]) -> list[Machine]:
    machines = []
    for line in data:
        if not line.strip():
            continue
        machines.append(Machine(line))
    return machines


def get_test_input_data() -> list[LiteralString]:
    data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    result = 0
    for m in data:
        logger.debug(m)
    return result


def part2() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
