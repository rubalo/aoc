# Advent of Code 2025 - Day 4

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


def get_input_data():
    return read_input(day=4, year=2025)


def parse_data(data: list[str]):
    parsed = []
    for line in data:
        if not line.strip():
            continue
        logger.debug(f"Parsing line: {line}")
        parsed_line = [x for x in line.strip()]
        parsed_line.append(".")  # Padding to avoid index errors
        parsed_line.insert(0, ".")  # Padding to avoid index errors
        parsed.append(parsed_line)
    parsed.insert(0, ["."] * len(parsed[0]))  # Top padding
    parsed.append(["."] * len(parsed[0]))  # Bottom padding
    return parsed


def get_test_input_data() -> list[LiteralString]:
    data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
    return data.split("\n")


def find_movable_rolls(data: list[list[str]]) -> list[complex]:
    movable_rolls = []
    for lin in range(1, len(data) - 1):
        for col in range(1, len(data[0]) - 1):
            pos = complex(col, lin)
            logger.debug(f"Checking position: {pos}")
            if data[lin][col] != "@":
                continue
            # Check adjacent positions
            # Up, Down, Left, Right, and Diagonals
            adjacent_positions = [
                pos + 1j,  # Up
                pos - 1j,  # Down
                pos - 1,  # Left
                pos + 1,  # Right
                pos + 1 + 1j,  # Up-Right
                pos + 1 - 1j,  # Down-Right
                pos - 1 + 1j,  # Up-Left
                pos - 1 - 1j,  # Down-Left
            ]
            adj_roll_count = 0
            for adj in adjacent_positions:
                if data[int(adj.imag)][int(adj.real)] == "@":
                    adj_roll_count += 1

            if adj_roll_count < 4:
                movable_rolls.append(pos)

    return movable_rolls


def print_floor(data: list[list[str]], movable_rolls: list[complex] = []) -> None:
    for lin in range(len(data)):
        line_str = ""
        for col in range(len(data[0])):
            if complex(col, lin) in movable_rolls:
                line_str += "X"
            else:
                line_str += data[lin][col]
        print(line_str)


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)
    rolls = find_movable_rolls(data)
    return len(rolls)


def part2() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)

    nb_movable_rolls = 0
    while True:
        rolls = find_movable_rolls(data)
        if not rolls:
            break
        nb_movable_rolls += len(rolls)
        for roll in rolls:
            data[int(roll.imag)][int(roll.real)] = "."
    return nb_movable_rolls
