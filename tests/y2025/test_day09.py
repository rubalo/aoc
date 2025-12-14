# Advent of Code 2025 - Day 9 - Test

from __future__ import annotations

import pytest

from aoc.y2025.day09 import (
    part1,
    part2,
)


def test_part1() -> None:
    assert part1() == 4764078684


@pytest.mark.skip(reason="Not implemented yet")
def test_part2() -> None:
    assert part2() == 1652344888
