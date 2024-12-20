# Advent of Code 2024 - Day 11

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=11, year=2024)


def parse_data(data: list[str]):
    return [int(x) for x in data[0].strip().split(" ")]


def get_test_input_data() -> list[LiteralString]:
    data = """125 17"""
    return data.split("\n")


def divide_stones(stone_number: int) -> list[int]:
    str_stone_number = str(stone_number)
    mid = len(str_stone_number) // 2
    stone_1 = str_stone_number[:mid]
    stone_2 = str_stone_number[mid:]

    return [int(stone_1), int(stone_2)]


def rules(stone_number: int) -> list[int]:
    if stone_number == 0:
        return [
            1,
        ]

    if len(str(stone_number)) % 2 == 0:
        return divide_stones(stone_number)

    return [
        stone_number * 2024,
    ]


def blink(stones: list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        new_stone = rules(stone)
        new_stones.extend(new_stone)
    return new_stones


def part1() -> int:
    data = get_input_data()
    stones = parse_data(data)
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


NB_CACHE_STONES = 100


def deep_first_compute(stone, depth, cache) -> int:
    if stone < NB_CACHE_STONES and stone in cache and depth in cache[stone]:
        return cache[stone][depth]

    if depth == 0:
        return 1

    stones = rules(stone)

    res = deep_first_compute(stones[0], depth - 1, cache)

    if len(stones) > 1:
        res += deep_first_compute(stones[1], depth - 1, cache)

    if stone < NB_CACHE_STONES:
        if stone not in cache:
            cache[stone] = {}

        cache[stone][depth] = res

    return res


def part2() -> int:
    data = get_input_data()
    stones = parse_data(data)

    res = 0
    for stone in stones:
        res += deep_first_compute(stone, 75, {})

    return res
