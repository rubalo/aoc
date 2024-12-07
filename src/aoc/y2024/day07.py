# Advent of Code 2024 - Day 7

from __future__ import annotations

from aoc.utils import read_input


class TestValidated(Exception):  # noqa
    pass


def get_input_data():
    data = read_input(day=7, year=2024)
    return parse_data(data)


def parse_data(data: list[str]):
    parsed_data = []
    lines = [x.strip() for x in data]
    for line in lines:
        r, n = line.split(":")
        ns = n.split(" ")
        parsed_data.append((int(r), [int(x) for x in ns if x]))
    return parsed_data


def get_test_input_data() -> list[str]:
    data = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    return parse_data(data.split("\n"))


def compute(n: int, ns: list[int], test_value: int):
    if len(ns) == 1:
        if n * ns[0] == test_value:
            raise TestValidated
        if n + ns[0] == test_value:
            raise TestValidated
        return 0

    compute(n * ns[0], ns[1:], test_value)
    compute(n + ns[0], ns[1:], test_value)

    return


def part1() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    res = 0
    for t_res, ns in data:
        try:
            compute(ns[0], ns[1:], t_res)
        except TestValidated:
            res += t_res
    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
