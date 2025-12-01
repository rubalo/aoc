# Advent of Code 2025 - Day 1

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=1, year=2025)


def parse_data(data: list[str]):
    parsed_data = [(line[0], int(line[1:])) for line in data if line.strip()]
    print(parsed_data)
    return parsed_data


def get_test_input_data() -> list[LiteralString]:
    data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)

    dial = 50
    cpt = 0

    for direction, amount in parsed_data:
        if direction == "L":
            dial -= amount
        elif direction == "R":
            dial += amount

        dial %= 100

        if dial == 0:
            cpt += 1

    return cpt


def part2() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    parsed_data = parse_data(data)

    dial = 50
    cpt = 0

    for direction, amount in parsed_data:
        cpt += amount // 100
        remainder = amount % 100
        if direction == "L":
            if dial - remainder < 0 and dial != 0:
                cpt += 1
            dial -= remainder
        elif direction == "R":
            if dial + remainder > 100 and dial != 0:
                cpt += 1
            dial += remainder
        dial %= 100

        if dial == 0:
            cpt += 1

    print(f"Final Dial: {dial}")
    return cpt
