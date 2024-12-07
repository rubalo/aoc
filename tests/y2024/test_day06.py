# Advent of Code 2024 - Day 6 - Test

from __future__ import annotations

import pytest

from aoc.y2024.day06 import part1, part2


def test_part1() -> None:
    assert part1() == 4776


@pytest.mark.skip("Brute force solution, takes too long")
def test_part2() -> None:
    assert part2() == 1586
