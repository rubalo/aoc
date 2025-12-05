# Advent of Code 2025 - Day 5

from __future__ import annotations

import logging
from typing import LiteralString, Tuple

from aoc.utils import read_input

logger = logging.getLogger(__name__)


class Range:
    start: int
    end: int

    def __init__(self, start: int, end: int):
        if start > end:
            self.start = end
            self.end = start
        else:
            self.start = start
            self.end = end

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end

    def __len__(self) -> int:
        return self.end - self.start + 1

    def __iter__(self):
        yield self.start
        yield self.end

    def __repr__(self):
        return f"Range({self.start}, {self.end})"

    def merge(self, r: Range) -> Range | None:
        """Merge two ranges if they overlap or are contiguous, else return None"""
        if self.end + 1 < r.start or r.end + 1 < self.start:
            return None
        new_start = min(self.start, r.start)
        new_end = max(self.end, r.end)
        return Range(new_start, new_end)

    def intersection(self, r: Range) -> Range | None:
        """Return the intersection of two ranges, or None if they don't intersect."""
        new_start = max(self.start, r.start)
        new_end = min(self.end, r.end)
        if new_start <= new_end:
            return Range(new_start, new_end)
        return None

    def union(self, r: Range) -> Range:
        """Return the union of two ranges."""
        new_start = min(self.start, r.start)
        new_end = max(self.end, r.end)
        return Range(new_start, new_end)


Ingredients = list[int]
Ranges = list[Range]
Input = Tuple[Ranges, Ingredients]


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

    return (ranges, ingredients)


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
    ranges, ingredients = input
    fresh_ingredients = []
    for ingredient in ingredients:
        is_fresh = any(ingredient in frange for frange in ranges)  # type: ignore
        if is_fresh:
            fresh_ingredients.append(ingredient)
    return fresh_ingredients


def process_ranges(ranges: Ranges) -> Ranges:
    if not ranges:
        return []

    # Sort ranges by start value
    sorted_ranges = sorted(ranges, key=lambda r: r.start)
    merged_ranges = [sorted_ranges[0]]

    for current in sorted_ranges[1:]:
        last_merged = merged_ranges[-1]
        merged = last_merged.merge(current)
        if merged:
            merged_ranges[-1] = merged
        else:
            merged_ranges.append(current)

    return merged_ranges


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    print(data)
    fresh_ingredients = get_freshness(data)
    print(f"Fresh ingredients: {fresh_ingredients}")
    return len(fresh_ingredients)


def part2() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    ranges = data[0]
    new_ranges = process_ranges(ranges)

    logger.debug(f"Processed ranges: {new_ranges}")
    nb_fresh_ingredients = 0

    for r in new_ranges:
        logger.debug(f"Processing range: {r} -> {len(r)}")
        nb_fresh_ingredients += len(r)

    return nb_fresh_ingredients
