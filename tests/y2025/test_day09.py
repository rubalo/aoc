# Advent of Code 2025 - Day 9 - Test

from __future__ import annotations

import pytest

from aoc.y2025.day09 import part1, part2, vector_cross_path


def test_vector_cross_path() -> None:
    v1 = (0 + 0j, 5 + 0j)
    path = [(1 + 1j, 1 + 5j)]
    assert vector_cross_path(v1, path) is False


def test_part1() -> None:
    assert part1() == 4764078684


@pytest.mark.skip(reason="Not implemented yet")
def test_part2() -> None:
    assert part2() == 0
