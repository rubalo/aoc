# Advent of Code 2024 - Day 3

from __future__ import annotations

import re

from aoc.utils import read_input


def get_input_data() -> list[str]:
    return read_input(day=3, year=2024)


def get_test_input_data() -> list[str]:
    return [""]


def part1() -> int:
    data = get_input_data()
    return multiply(data)


def multiply(data: list[str]) -> int:
    parser = re.compile(r"mul\((\d+),(\d+)\)")
    res = 0

    for line in data:
        match = parser.findall(line)
        for x, y in match:
            res += int(x) * int(y)
    return res


def clean_data(data: str) -> str:
    inner = True

    dont_pattern = re.compile(r"don't\(\)")
    do_pattern = re.compile(r"do\(\)")

    dont_pos = [x.span()[0] for x in dont_pattern.finditer(data)]
    do_pos = [x.span()[0] for x in do_pattern.finditer(data)]

    res = ""
    for i, char in enumerate(data):
        if i in do_pos:
            inner = True
        if i in dont_pos:
            inner = False
        if inner:
            res += char

    return res


def part2() -> int:
    data = get_input_data()
    j_data = "".join([x.rstrip() for x in data])

    c_data = [
        clean_data(j_data),
    ]

    return multiply(c_data)
