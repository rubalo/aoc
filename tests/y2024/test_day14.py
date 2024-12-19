# Advent of Code 2024 - Day 14 - Test

from __future__ import annotations
import pytest

from aoc.y2024.day14 import part1, part2


def test_part1() -> None:
    assert part1() == 230435667


@pytest.mark.skip("Test takes too long")
def test_part2() -> None:
    assert part2() == 7709
