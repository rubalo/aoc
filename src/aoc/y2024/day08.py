# Advent of Code 2024 - Day 8

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import read_input


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


D = {}
DATA = get_input_data()

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


def get_frequency_antinodes(part: int):
    for key in D:
        get_antenas_antinodes(D[key], part)


def get_antenas_antinodes(antenna: list, part: int):
    for i, a in enumerate(antenna):
        for j, b in enumerate(antenna):
            if i == j:
                continue
            if part == 1:
                get_antinodes_1(a, b)
            else:
                get_antinodes_2(a, b)


def get_antinodes_1(a: complex, b: complex):
    v = a - b
    anti_a = a + v
    anti_b = b - v
    add_antinode(anti_a)
    add_antinode(anti_b)


def get_antinodes_2(a: complex, b: complex):
    v = a - b
    anti_a = a + v
    anti_b = b - v
    add_antinode(a)
    add_antinode(b)
    while add_antinode(anti_a):
        anti_a += v
    while add_antinode(anti_b):
        anti_b -= v


def add_antinode(v: complex) -> bool:
    x, y = int(v.real), int(v.imag)
    if x < 0 or y < 0 or x >= DATA.shape[0] or y >= DATA.shape[1]:
        return False

    ANTINODES.add(v)
    if DATA[x, y] == ".":
        DATA[x, y] = "#"

    return True


def part1() -> int:
    global ANTINODES  # noqa
    ANTINODES = set()
    print_data()
    parse_antennas()
    get_frequency_antinodes(part=1)
    print_data()
    return len(ANTINODES)


def part2() -> int:
    global ANTINODES  # noqa
    ANTINODES = set()
    print_data()
    parse_antennas()
    get_frequency_antinodes(part=2)
    print_data()
    return len(ANTINODES)
