# Advent of Code 2025 - Day 3

from __future__ import annotations

import logging
from typing import LiteralString

from aoc.utils import read_input

NB_BATTERIES_PART1 = 2
NB_BATTERIES_PART2 = 12


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


def find_joltages(banks: list[list[int]], nb_batteries: int) -> list[int]:
    joltages = []
    for bank in banks:
        joltages.append(find_joltage(bank, nb_batteries))
    return joltages


def find_joltage(bank: list[int], nb_batteries: int) -> int:
    bats = [0] * nb_batteries
    bats_indexes = [x for x in range(nb_batteries)]
    logger.debug(f"Finding joltage for bank: {bank}")

    for i in range(nb_batteries):
        # Look for the biggest jolt for first digit
        logger.debug(f"--- Bat {i}/{nb_batteries} ---")
        logger.debug(f"Bats         : {bats}")
        logger.debug(f"Bats indexes : {bats_indexes}")
        logger.debug(
            f"Range is from {bats_indexes[i]} to {len(bank) - nb_batteries + i}"
        )
        for j in range(bats_indexes[i], len(bank) - nb_batteries + i + 1):
            logger.debug(f"Considering bank[{j}] = {bank[j]}")
            if bank[j] > bats[i]:
                bats[i] = bank[j]
                bats_indexes[i] = j + 1
                bats_indexes[i + 1 :] = [
                    k
                    for k in range(
                        bats_indexes[i], bats_indexes[i] + nb_batteries - i - 1
                    )
                ]
                logger.debug(f"  New bat value: {bats[i]}")

    logger.debug(f"Final bats: {bats}")
    joltage = int("".join(str(bat) for bat in bats))
    return joltage


def part1() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)
    print(parsed_data)
    joltages = find_joltages(parsed_data, NB_BATTERIES_PART1)
    print(joltages)
    return sum(joltages)


def part2() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)
    print(parsed_data)
    joltages = find_joltages(parsed_data, NB_BATTERIES_PART2)
    print(joltages)
    return sum(joltages)
    return 0
