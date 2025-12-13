# Advent of Code 2025 - Day 9 - Test

from __future__ import annotations

import pytest

from aoc.y2025.day09 import part1, part2, point_in_path, vector_crosses_path


def test_point_on_path() -> None:
    path = [(1 + 1j), (5 + 1j), (5 + 5j), (1 + 5j)]

    for p in path:
        assert point_in_path(p, path) is True

    for p in [(0 + 0j), (6 + 6j), (3 + 0j), (0 + 3j), (6 + 3j), (3 + 6j)]:
        assert point_in_path(p, path) is False

    for p in [(3 + 1j), (5 + 3j), (3 + 5j), (1 + 3j)]:
        assert point_in_path(p, path) is True


def test_vector_cross_path() -> None:
    path = [
        (0 + 0j),
        (5 + 5j),
        (1 + 5j),
        (1 + 3j),
        (2 + 3j),
        (2 + 5j),
        (5 + 5j),
        (5 + 0j),
    ]

    vector1 = (
        (0 + 4j),
        (5 + 4j),
    )

    vector2 = (
        (0 + 3j),
        (5 + 3j),
    )

    assert vector_crosses_path(vector1[0], vector1[1], path) is True
    assert vector_crosses_path(vector2[0], vector2[1], path) is False


def test_part1() -> None:
    assert part1() == 4764078684


@pytest.mark.skip(reason="Not implemented yet")
def test_part2() -> None:
    assert part2() == 1652344888
