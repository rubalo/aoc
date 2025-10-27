# Advent of Code 2024 - Day 22 - Test

from __future__ import annotations

from aoc.y2024.day22 import part1, part2


def test_part1() -> None:
    assert part1() == 20401393616


def test_part2() -> None:
    assert part2() == 2272
