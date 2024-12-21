# Advent of Code 2024 - Day 16 - Test

from __future__ import annotations

from aoc.y2024.day16 import part1, part2


def test_part1() -> None:
    assert part1() == 98520


def test_part2() -> None:
    assert part2() == 609
