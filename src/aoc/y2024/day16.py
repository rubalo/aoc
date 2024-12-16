# Advent of Code 2024 - Day 16

from __future__ import annotations
from collections import deque
from typing import LiteralString
from aoc.utils import read_input

import numpy as np

UP = complex(-1,0)
DOWN = complex(1,0)
LEFT = complex(0,-1)
RIGHT = complex(0, 1)

def get_input_data():
    return read_input(day=16, year=2024)


def parse_data(data: list[str]):
    return np.array([np.array(list(x)) for x in data])

def get_test_input_data() -> list[LiteralString]:
    data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    return data.split("\n")

def print_map(mapp: np.arrray, pos=None, direction=None, visited = None):

    data = mapp.copy()
    if pos:
        xp, yp = get_pos(pos)
        if direction == UP:
            cursor = "^"
        if direction == DOWN:
            cursor = "v"
        if direction == LEFT:
            cursor = "<"
        if direction == RIGHT:
            cursor = ">"

        data[xp, yp] = cursor

    if visited:
        for path in visited:
            xv, yv = get_pos(path)
            data[xv, yv] = "X"

    for i in range(len(data)):
        for j in range(len(data[0])):
                print(data[i,j], end ="")
        print()


def find_start_end(mapp: np.array) -> tuple[complex, complex]:
    start, end = None, None

    for i, row in enumerate(mapp):
        try:
            start = complex(i, list(row).index("S"))
        except ValueError:
            pass
        try:
            end = complex(i, list(row).index("E"))
        except ValueError:
            pass
    if not start or not end:
        raise ValueError

    return start, end

def get_val(pos: complex, data):
    x, y = get_pos(pos)
    try:
        return data[x,y] if data[x,y] != "#" else None
    except IndexError:
        breakpoint()

def get_pos(val: complex):
    return int(val.real), int(val.imag)


def get_neighbours(pos, direction, score, data):
    neighbours = []
    r_dir = direction

    for i in range(4):
        if get_val(pos + r_dir, data) != None:
            neighbours.append((pos + r_dir, r_dir, score + (i * 1000) +1))
        r_dir = r_dir * 1j

    return neighbours




PREC = {}
Q = deque()

def walk():

    pos, direction, score, stop, data = Q.pop()

    neighbours = get_neighbours(pos, direction, score, data)

    for neighbour in neighbours:
        n_pos, n_dir, n_score = neighbour
        if not (n_pos, n_dir) in PREC:
            PREC[(n_pos, n_dir)] = (pos, direction, n_score)
        elif n_score < PREC[(n_pos, n_dir)][2]:
            PREC[(n_pos, n_dir)] = (pos, direction, n_score)

        Q.append((n_pos, n_dir, n_score, stop, data))



def part1() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()
    mapp = parse_data(data)
    print_map(mapp)
    start, end = find_start_end(mapp)
    print(start, end)

    Q.append((start, complex(0,1), 0, end, mapp))

    while len(Q) > 0:
        walk()

    print(PREC)

    return 0


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
