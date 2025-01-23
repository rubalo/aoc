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

    # Res = 19
    data = """...........#.....#......
...................#....
...#.....##.............
......................#.
..................#.....
..#.....................
....................#...
........................
.#........^.............
..........#..........#..
..#.....#..........#....
........#.....#..#......"""
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


def get_guard_path(
    g_s_pos: complex, d: D, data: np.array, mark: str = "X"
) -> list[tuple[complex, D]]:
    g_pos = g_s_pos

    guard_path = [
        (g_pos, d),
    ]

    while True:
        n_coord = g_pos + d.value
        n_x, n_y = int(n_coord.real), int(n_coord.imag)

        if not (0 <= n_x < data.shape[0] and 0 <= n_y < data.shape[1]):
            break

        if data[n_x, n_y] in ["#", "0"]:
            d = D(d.value * -1j)
            continue

        # move forward
        g_pos += d.value
        if (g_pos, d) in guard_path:
            raise ValueError

        guard_path.append((g_pos, d))

        # Mark the start posityion in blue
        if g_pos == g_s_pos:
            data[int(g_pos.real), int(g_pos.imag)] = "^"
        else:
            data[int(g_pos.real), int(g_pos.imag)] = mark

    return guard_path


def part1() -> int:
    data = get_input_data()
    g_pos, d = find_guard(data)
    guard_path = get_guard_path(g_pos, d, data)
    guard_poss = {g for g, _ in guard_path}
    return len(guard_poss)


def part2() -> int:
    data = get_input_data()
    res = 0
    g_pos, d = find_guard(data)

    data_1 = data.copy()
    guard_path = get_guard_path(g_pos, d, data_1)

    obstacles = set()

    cpt = 0
    for pg, _ in guard_path[1:]:
        data_w_obs = data.copy()

        if pg == g_pos:
            continue

        if pg in obstacles:
            continue

        x, y = int(pg.real), int(pg.imag)

        obstacles.add(pg)
        try:
            data_w_obs[x, y] = "0"
            get_guard_path(g_pos, d, data_w_obs, mark="*")
        except ValueError:
            res += 1
        cpt += 1

    return res
