# Advent of Code 2025 - Day 9 - Test

from __future__ import annotations

from aoc.y2025.day09 import (
    game_data,
    get_horizontal_boudaries,
    get_vertical_boudaries,
    part1,
    part2,
)


def test_get_horizontal_boudaries() -> None:
    """data = [
        "...........",
        ".####....##",
        ".#..#....##",
        ".#..#######",
        ".#........#",
        ".##########",
        "...........",
    ]"""

    path = [
        (1 + 1j),
        (4 + 1j),
        (4 + 3j),
        (9 + 3j),
        (9 + 1j),
        (10 + 1j),
        (10 + 5j),
        (1 + 5j),
    ]

    expected = {
        0: [],
        1: [(1, 4), (9, 10)],
        2: [(1, 4), (9, 10)],
        3: [(1, 10)],
        4: [(1, 10)],
        5: [(1, 10)],
        6: [],
    }

    game_data(path)

    for level, result in expected.items():
        assert (
            get_horizontal_boudaries(path, level) == result
        ), f"Error at level {level}"


def test_get_vertical_boudaries() -> None:
    """
    data = [
        "...........",
        ".####....##",
        ".#..#....##",
        ".#..#######",
        ".#........#",
        ".##########",
        "...........",
    ]"""

    path = [
        (1 + 1j),
        (4 + 1j),
        (4 + 3j),
        (9 + 3j),
        (9 + 1j),
        (10 + 1j),
        (10 + 5j),
        (1 + 5j),
    ]

    expected = {
        0: [],
        1: [(1, 5)],
        2: [(1, 5)],
        3: [(1, 5)],
        4: [(1, 5)],
        5: [(3, 5)],
        8: [(3, 5)],
        9: [(1, 5)],
        10: [(1, 5)],
        11: [],
    }
    game_data(path)

    for level, result in expected.items():
        assert get_vertical_boudaries(path, level) == result, f"Error at level {level}"


def test_get_vertical_boundaries2() -> None:
    """
    data = [
                   1
         01234567890
      0 "...........",
      1 ".##########",
      2 ".#........#",
      3 ".#........#",
      4 ".#........#",
      5 ".########.#",
      6 "........#.#",
      7 ".########.#",
      8 ".#........#",
      9 ".#........#",
     10 ".#....#####",
     11 ".#....#....",
     12 ".######....",
                   1
         01234567890

    ]"""

    path = [
        (1 + 1j),
        (10 + 1j),
        (10 + 10j),
        (6 + 10j),
        (6 + 12j),
        (1 + 12j),
        (1 + 7j),
        (8 + 7j),
        (8 + 5j),
        (1 + 5j),
    ]

    expected = {
        6: [(1, 5), (7, 12)],
    }

    game_data(path)

    for level, result in expected.items():
        assert get_vertical_boudaries(path, level) == result, f"Error at level {level}"


def test_part1() -> None:
    assert part1() == 4764078684


def test_part2() -> None:
    assert part2() == 1652344888
