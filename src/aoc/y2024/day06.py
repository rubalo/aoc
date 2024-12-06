# Advent of Code 2024 - Day 6

from __future__ import annotations

import enum

import numpy as np

from aoc.utils import read_input


def get_input_data():
    data = read_input(day=6, year=2024)
    return parse_data(data)


def parse_data(data: list[str]):
    return np.array([np.array(list(row)) for row in data])


def get_test_input_data() -> list[str]:
    data = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    return parse_data(data.splitlines())


class D(enum.Enum):
    up = -1 + 0j
    down = 1 + 0j
    left = -1j
    right = 1j


def find_guard(data: np.array) -> tuple[complex, D] | None:
    for i, row in enumerate(data):
        for j, col in enumerate(row):
            if col == "^":
                return complex(i, j), D.up
            if col == ">":
                return complex(i, j), D.right
            if col == "v":
                return complex(i, j), D.down
            if col == "<":
                return complex(i, j), D.left
    return None


def part1() -> int:
    data = get_input_data()
    res = 1

    g_pos, d = find_guard(data)
    x, y = int(g_pos.real), int(g_pos.imag)

    while True:
        n_coord = g_pos + d.value
        n_x, n_y = int(n_coord.real), int(n_coord.imag)

        if not (0 <= n_x < data.shape[0] and 0 <= n_y < data.shape[1]):
            break

        if data[n_x, n_y] == "#":
            d = D(d.value * -1j)
            continue

        if data[n_x, n_y] == ".":
            res += 1

        # move forward
        g_pos += d.value
        # update position
        x, y = int(g_pos.real), int(g_pos.imag)
        data[x, y] = "X"

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
