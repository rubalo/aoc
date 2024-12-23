# Advent of Code 2024 - Day 18 - Test

from __future__ import annotations

from aoc.y2024.day18 import part1, part2


def test_part1() -> None:
    assert part1() == 248


def test_part2() -> None:
    assert part2() == "32,55"
