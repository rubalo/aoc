# Advent of Code 2024 - Day 8

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import read_input

D = {}
DATA = np.array([])
ANTINODES = set()


def get_input_data():
    data = read_input(day=8, year=2024)
    return parse_data(data)


def parse_data(data: list[str]):
    return np.array([np.array(list(x.rstrip())) for x in data])


def get_test_input_data() -> list[LiteralString]:
    data = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    return parse_data(data.split("\n"))


def parse_antennas():
    for i, row in enumerate(DATA):
        for j, _ in enumerate(row):
            if DATA[i, j] == ".":
                continue

            antenna = str(DATA[i, j])
            if antenna not in D:
                D[antenna] = []

            D[antenna].append(i + j * 1j)


def print_data():
    for row in DATA:
        print("".join(row))  # noqa


def get_frequency_antinodes():
    for key in D:
        get_antenas_antinodes(D[key])


def get_antenas_antinodes(antenna: list):
    for i, a in enumerate(antenna):
        for j, b in enumerate(antenna):
            if i == j:
                continue
            get_antinodes(a, b)


def get_antinodes(a: complex, b: complex):
    v = a - b
    anti_a = a + v
    anti_b = b - v
    add_antinode(anti_a)
    add_antinode(anti_b)


def add_antinode(v: complex):
    x, y = int(v.real), int(v.imag)
    if x < 0 or y < 0 or x >= DATA.shape[0] or y >= DATA.shape[1]:
        return
    ANTINODES.add(v)
    if DATA[x, y] == ".":
        DATA[x, y] = "#"


def part1() -> int:
    global DATA  # noqa
    DATA = get_input_data()
    print_data()
    parse_antennas()
    get_frequency_antinodes()
    print_data()
    return len(ANTINODES)


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
