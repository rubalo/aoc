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


def find_x_pattern(matrix: np.array) -> int:
    res = 0

    if matrix.shape != (3, 3):
        return res

    # First check
    res += check_pattern(matrix)

    # Rotate 90 degrees
    matrix = np.rot90(matrix)
    res += check_pattern(matrix)

    # Rotate 180 degrees
    matrix = np.rot90(matrix)
    res += check_pattern(matrix)

    # Rotate 270 degrees
    matrix = np.rot90(matrix)
    res += check_pattern(matrix)

    return res


def check_pattern(matrix: np.array) -> int:
    if (
        matrix[0][0] == "M"
        and matrix[1][1] == "A"
        and matrix[2][2] == "S"
        and matrix[2][0] == "M"
        and matrix[0][2] == "S"
    ):
        return 1
    return 0


def part2() -> int:
    data = get_input_data()
    matrix = np.array([list(x) for x in data])

    res = 0

    for i in range(matrix.shape[0] - 2):
        for j in range(matrix.shape[1] - 2):
            res += find_x_pattern(matrix[i : i + 3, j : j + 3])

    return res
