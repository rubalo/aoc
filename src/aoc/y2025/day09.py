# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


def get_input_data():
    return read_input(day=9, year=2025)


def parse_data(data: list[str]) -> list[complex]:
    input = []
    for line in data:
        if line.strip() == "":
            continue

        x, y = line.split(",")
        input.append(complex(int(x), int(y)))

    return input


def get_test_input_data() -> list[LiteralString]:
    data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
    return data.split("\n")


def draw(data: list[complex]) -> None:
    min_x = 0
    min_y = 0
    max_x = int(max(p.real for p in data)) + 2
    max_y = int(max(p.imag for p in data)) + 1

    grid = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            if complex(x, y) in data:
                row.append("#")
            else:
                row.append(".")
        grid.append("".join(row))

    for row in grid:
        print(row)


def compute_surfaces(data: list[complex]) -> tuple[complex, complex, int]:
    max_surface = 0
    max_p1 = 0 + 0j
    max_p2 = 0 + 0j
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            p1 = data[i]
            p2 = data[j]

            width = abs(p2.real - p1.real) + 1
            height = abs(p2.imag - p1.imag) + 1
            area = width * height
            logger.debug(f"Area between {p1} and {p2}: {area}")
            if area > max_surface:
                max_surface = area
                max_p1 = p1
                max_p2 = p2

    logger.info(f"Max surface: {max_surface} between points {max_p1} and {max_p2}")

    return max_p1, max_p2, int(max_surface)


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    _, _, max_surface = compute_surfaces(data)
    return max_surface


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
