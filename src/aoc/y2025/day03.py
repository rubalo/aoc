# Advent of Code 2025 - Day 3

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def get_input_data():
    return read_input(day=3, year=2025)


def parse_data(data: list[str]) -> list[list[int]]:
    parsed_data = []
    for line in data:
        parsed_line = [int(char) for char in line.strip()]
        parsed_data.append(parsed_line)

    return parsed_data


def get_test_input_data() -> list[LiteralString]:
    data = """987654321111111
811111111111119
234234234234278
818181911112111
"""
    return data.split("\n")


def find_joltages(banks: list[list[int]]) -> list[int]:
    joltages = []
    for bank in banks:
        joltages.append(find_joltage(bank))
    return joltages


def find_joltage(bank: list[int]) -> int:
    ten = 0
    unit = 0
    logger.debug(f"Finding joltage for bank: {bank}")
    for i in range(len(bank)):
        if i < len(bank) - 1 and bank[i] > ten:
            ten = bank[i]
            unit = bank[i + 1]
            logger.debug(f"New ten: {ten}, unit: {unit}")
        elif bank[i] > unit:
            unit = bank[i]
            logger.debug(f"New unit: {unit}")
    return int(str(ten) + str(unit))


def part1() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)
    print(parsed_data)
    joltages = find_joltages(parsed_data)
    print(joltages)
    return sum(joltages)


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()
    parsed_data = parse_data(data)
    print(parsed_data)
    joltages = find_joltages(parsed_data)
    print(joltages)
    return sum(joltages)
    return 0
