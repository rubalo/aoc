# Advent of Code 2024 - Day 1 - Test

from __future__ import annotations

from aoc.y2024.day01 import part1, part2


def test_part1() -> None:
    assert part1() == 1197984


def test_part2() -> None:
    assert part2() == 23387399
