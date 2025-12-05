# Advent of Code 2025 - Day 5

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


class Range:
    __slots__ = ("start", "end")

    def __init__(self, start: int, end: int):
        if not all(isinstance(i, int) for i in (start, end)):
            raise TypeError("Start and end must be integers")
        self.start = start if start <= end else end
        self.end = end if end >= start else start

    def __iter__(self):
        yield self.start
        yield self.end

    def __repr__(self):
        return f"Range({self.start}, {self.end})"

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end


Ingredients = list[int]
Ranges = list[Range]
Input = dict[str, Ranges | Ingredients]


def get_input_data():
    return read_input(day=5, year=2025)


def parse_data(data: list[str]) -> Input:
    ranges = []
    ingredients = []

    while len(data):
        line = data.pop(0).strip()
        if line == "":
            break
        logger.debug(f"Parsing line: {line}")
        # Process range lines here
        # e.g., "3-5" -> (3, 5)
        x, y = map(int, line.split("-"))
        logger.debug(f"Parsed range: {x} to {y}")
        ranges.append(Range(x, y))

    while len(data):
        line = data.pop(0).strip()
        if line == "":
            continue
        logger.debug(f"Parsing test input line: {line}")
        # Process test input lines here
        value = int(line)
        logger.debug(f"Parsed test input value: {value}")
        ingredients.append(value)

    return {
        "ranges": ranges,
        "ingredients": ingredients,
    }


def get_test_input_data() -> list[LiteralString]:
    data = """3-5
    10-14
    16-20
    12-18

    1
    5
    8
    11
    17
    32
"""
    return data.split("\n")


def get_freshness(input: Input) -> list[int]:
    ranges, ingredients = input["ranges"], input["ingredients"]
    fresh_ingredients = []
    for ingredient in ingredients:
        is_fresh = any(ingredient in frange for frange in ranges)  # type: ignore
        if is_fresh:
            fresh_ingredients.append(ingredient)
    return fresh_ingredients


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    print(data)
    fresh_ingredients = get_freshness(data)
    print(f"Fresh ingredients: {fresh_ingredients}")
    return len(fresh_ingredients)


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
