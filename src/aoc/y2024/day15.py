# Advent of Code 2024 - Day 15

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import read_input

UP = complex(-1, 0)
DOWN = complex(1, 0)
LEFT = complex(0, 1)
RIGHT = complex(0, -1)


def get_input_data():
    return read_input(day=15, year=2024)


def parse_data(data: list[str]):
    sep = data.index("")
    mapp = parse_map(data[:sep])
    moves = parse_moves(data[sep + 1 :])
    return mapp, moves


def parse_map(data: list[str]):
    return np.array([np.array(list(x.strip())) for x in data])


def parse_moves(data: list[str]):
    raw_list = "".join([x.strip() for x in data])
    return [parse_move(x) for x in raw_list]


def parse_move(move: str) -> complex:
    if move == "^":
        return UP
    if move == "v":
        return DOWN
    if move == ">":
        return LEFT
    if move == "<":
        return RIGHT

    print(move)  # noqa

    raise IndexError


def get_test_input_data() -> list[LiteralString]:
    data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    #     data = """########
    # #..O.O.#
    # ##@.O..#
    # #...O..#
    # #.#.O..#
    # #...O..#
    # #......#
    # ########
    #
    # <^^>>>vv<v>>v<<"""
    return data.split("\n")


def print_map(mapp: np.array):
    for i in range(len(mapp)):
        for j in range(len(mapp[0])):
            print(mapp[i, j], end="")  # noqa
        print()  # noqa


def find_robot(data: np.array) -> complex:
    for i, row in enumerate(data):
        try:
            return complex(i, list(row).index("@"))
        except ValueError:
            continue

    raise IndexError


def move(row: list[complex], direction: complex, data: np.array) -> np.array:
    dest: complex = row[-1] + direction
    x, y = int(dest.real), int(dest.imag)

    if data[x, y] == "#":
        # Hit the wall, cannot push !
        return data

    if data[x, y] == "O":
        # Hit a case, try to move it also
        row.append(dest)
        return move(row, direction, data)

    if data[x, y] == ".":
        # Move all the list
        cx, cy = x, y
        ox, oy = 0, 0
        while len(row) != 0:
            item = row.pop()
            ox, oy = int(item.real), int(item.imag)
            data[cx, cy] = data[ox, oy]
            cx, cy = ox, oy
        data[ox, oy] = "."

        return data

    raise ValueError


def get_coord(mapp: np.array) -> int:
    res = 0
    for i in range(len(mapp)):
        for j in range(len(mapp[0])):
            if mapp[i, j] == "O":
                res += i * 100 + j

    return res


def part1() -> int:
    data = [x.strip() for x in get_input_data()]
    # data = get_test_input_data()
    mapp, moves = parse_data(data)
    print_map(mapp)
    print()  # noqa

    robot = find_robot(mapp)
    print(robot)  # noqa
    for n_move in moves:
        mapp = move([robot], n_move, mapp)
        robot = find_robot(mapp)
        # print_map(mapp)

    return get_coord(mapp)


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
