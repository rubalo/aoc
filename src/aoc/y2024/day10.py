# Advent of Code 2024 - Day 10

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import read_input


def get_input_data():
    return read_input(day=10, year=2024)


def parse_data(data: list[str]):
    return np.array([np.array([int(y) for y in x.strip()]) for x in data])


def get_test_input_data() -> list[LiteralString]:
    data = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    return data.split("\n")


UP = -1 + 0j
DOWN = 1 + 0j
LEFT = 0 - 1j
RIGHT = 0 + 1j


def walk(data, i, j, direction, trail_id):
    i1 = i + int(direction.real)
    j1 = j + int(direction.imag)
    if i1 < 0 or i1 >= len(data) or j1 < 0 or j1 >= len(data[0]):
        return
    if data[i1, j1] != data[i, j] + 1:
        return
    if data[i1, j1] == 9:  # noqa
        TRAILS.add((trail_id, i1, j1))
    find_trails(data, i1, j1, trail_id)


def find_trails(data, i, j, trail_id):
    walk(data, i, j, UP, trail_id)
    walk(data, i, j, DOWN, trail_id)
    walk(data, i, j, LEFT, trail_id)
    walk(data, i, j, RIGHT, trail_id)


def walk2(data, i, j, direction):
    i1 = i + int(direction.real)
    j1 = j + int(direction.imag)
    if i1 < 0 or i1 >= len(data) or j1 < 0 or j1 >= len(data[0]):
        return 0
    if data[i1, j1] != data[i, j] + 1:
        return 0
    if data[i1, j1] == 9:  # noqa
        return 1
    return find_trails2(data, i1, j1)


def find_trails2(data, i, j):
    return sum(
        [
            walk2(data, i, j, UP),
            walk2(data, i, j, DOWN),
            walk2(data, i, j, LEFT),
            walk2(data, i, j, RIGHT),
        ]
    )


TRAILS = set()


def count_trails():
    return len(TRAILS)


def part1() -> int:
    r_data = get_input_data()
    # r_data = get_test_input_data()
    data = parse_data(r_data)
    cpt = 1
    for i, row in enumerate(data):
        for j, _ in enumerate(row):
            if data[i, j] == 0:
                find_trails(data, i, j, cpt)
                cpt += 1
    return count_trails()


def part2() -> int:
    r_data = get_input_data()
    # r_data = get_test_input_data()
    data = parse_data(r_data)
    cpt = 1
    res = 0
    for i, row in enumerate(data):
        for j, _ in enumerate(row):
            if data[i, j] == 0:
                trail_count = find_trails2(data, i, j)
                cpt += 1
                res += trail_count
    return res
