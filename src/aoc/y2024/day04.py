# Advent of Code 2024 - Day 4

from __future__ import annotations

import re

import numpy as np

from aoc.utils import read_input

pattern = re.compile("(?=(XMAS|SAMX))")


def get_input_data() -> list[str]:
    return read_input(day=4, year=2024)


def get_test_input_data() -> list[str]:
    data = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    return [str(x) for x in data.split("\n")]


def count_horizontal_patterns(matrix: np.array) -> int:
    res = 0
    for i in range(matrix.shape[0]):
        line = matrix[i]
        match = pattern.findall("".join(line))
        res += len(match)
    return res


def count_vertical_patterns(matrix: np.array) -> int:
    return count_horizontal_patterns(matrix.T)


def count_diagonal_patterns(matrix: np.array) -> int:
    res = 0
    for x in range((matrix.shape[1] - 1) * -1, matrix.shape[0] - 1):
        line = matrix.diagonal(x)
        res += count_horizontal_patterns(np.array([line]))
    return res


def count_anti_diagonal_patterns(matrix: np.array) -> int:
    return count_diagonal_patterns(np.fliplr(matrix))


def part1() -> int:
    data = get_input_data()
    matrix = np.array([list(x) for x in data])

    # Horizontal
    res = count_horizontal_patterns(matrix)

    # Vertical
    res += count_vertical_patterns(matrix)

    # Diagonal
    res += count_diagonal_patterns(matrix)

    # Anti-Diagonal
    res += count_anti_diagonal_patterns(matrix)

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
