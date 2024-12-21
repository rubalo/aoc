# Advent of Code 2024 - Day 17 - Test

from __future__ import annotations

from aoc.y2024.day17 import part1, part2


def test_part1() -> None:
    assert part1() == "2,0,7,3,0,3,1,3,7"


def test_part2() -> None:
    assert part2() == 0
