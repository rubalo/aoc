# Advent of Code 2024 - Day 15

from __future__ import annotations

from collections import deque
from typing import LiteralString

import numpy as np

from aoc.utils import read_input

UP = complex(-1, 0)
DOWN = complex(1, 0)
LEFT = complex(0, 1)
RIGHT = complex(0, -1)


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_input_data():
    return read_input(day=15, year=2024)


def parse_data_p1(data: list[str]) -> tuple[np.array, list[complex]]:
    sep = data.index("")
    mapp = parse_map(data[:sep])
    moves = parse_moves(data[sep + 1 :])
    return mapp, moves


def parse_data_p2(data: list[str]) -> tuple[np.array, list[complex]]:
    sep = data.index("")
    mapp = parse_map2(data[:sep])
    moves = parse_moves(data[sep + 1 :])
    return mapp, moves


def parse_map(data: list[str]):
    return np.array([np.array(list(x.strip())) for x in data])


def parse_map2(data: list[str]):
    new_lines = []
    for line in data:
        new_line = []
        for char in line.strip():
            if char == "#":
                new_line.append("##")
            elif char == ".":
                new_line.append("..")
            elif char == "O":
                new_line.append("[]")
            elif char == "@":
                new_line.append("@.")

        new_lines.append(np.array(list("".join(new_line))))

    return np.array(new_lines)


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


def print_map(mapp: np.array, pos: complex | None = None) -> None:
    for i in range(len(mapp)):
        for j in range(len(mapp[0])):
            if pos is not None and complex(i, j) == pos:
                print(BCOLORS.FAIL + mapp[i, j] + BCOLORS.ENDC, end="")  # noqa
            else:
                print(mapp[i, j], end="")  # noqa
        print()  # noqa


def find_robot(data: np.array) -> complex:
    for i, row in enumerate(data):
        try:
            return complex(i, list(row).index("@"))
        except ValueError:
            continue

    raise IndexError


def find_robot2(data: np.array) -> complex:
    for i, row in enumerate(data):
        for j, item in enumerate(row):
            if item == "@":
                return complex(i, j)

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


def move2(s_pos: complex, direction: complex, data: np.array) -> np.array:
    visited = set()
    neighbours = deque()
    neighbours.append(s_pos)
    while len(neighbours) != 0:
        current_pos = neighbours.popleft()
        n_pos = current_pos + direction

        x_n, y_n = int(n_pos.real), int(n_pos.imag)

        if data[x_n, y_n] == "#":
            # we hit a wall, pushing is not possible
            return data

        if data[x_n, y_n] == "[" and direction in [UP, DOWN]:
            # we hit a case, try to move it also
            neighbours.append(n_pos)
            neighbours.append(n_pos + LEFT)
            visited.add(current_pos)
            continue

        if data[x_n, y_n] == "]" and direction in [UP, DOWN]:
            # we hit a case, try to move it also
            neighbours.append(n_pos)
            neighbours.append(n_pos + RIGHT)
            visited.add(current_pos)
            continue

        if (data[x_n, y_n] == "[" or data[x_n, y_n] == "]") and direction in [
            LEFT,
            RIGHT,
        ]:
            # we hit a case, try to move it also
            visited.add(current_pos)
            visited.add(n_pos)
            neighbours.append(n_pos + direction)
            continue

        if data[x_n, y_n] == ".":
            # Cool, it means we can move
            visited.add(current_pos)
            continue

    # If we reach this point, it means we have to move all the cases
    # Sort list by x if direction is UP or DOWN, by y if direction is LEFT or RIGHT
    if direction in [UP, DOWN]:
        visited = sorted(visited, key=lambda x: x.real)
        if direction == DOWN:
            visited = visited[::-1]
    else:
        visited = sorted(visited, key=lambda x: x.imag)
        if direction == LEFT:
            visited = visited[::-1]

    for pos in visited:
        x, y = int(pos.real), int(pos.imag)
        value = data[x, y]
        data[x, y] = "."
        data[x + int(direction.real), y + int(direction.imag)] = value

    return data


def get_coord(mapp: np.array, box_str="O") -> int:
    res = 0
    for i in range(len(mapp)):
        for j in range(len(mapp[0])):
            if mapp[i, j] == box_str:
                res += i * 100 + j

    return res


def part1() -> int:
    data = [x.strip() for x in get_input_data()]
    # data = get_test_input_data()
    mapp, moves = parse_data_p1(data)
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
    data = [x.strip() for x in get_input_data()]
    mapp, moves = parse_data_p2(data)
    print_map(mapp)
    for n_move in moves:
        robot = find_robot2(mapp)
        mapp = move2(robot, n_move, mapp)
    return get_coord(mapp, box_str="[")
