# Advent of Code 2023 - Day 20 - Test

from __future__ import annotations

from aoc.y2023.day20 import part1, part2


def test_part1() -> None:
    assert part1() == 712543680


def test_part2() -> None:
    assert part2() == 238920142622879
