# Advent of Code 2024 - Day 1

from __future__ import annotations

from collections import defaultdict

from aoc.utils import read_input


def get_input_data() -> list[str]:
    return read_input(day=1, year=2024)


def get_test_input_data() -> list[str]:
    return [""]


def parse(data: list[str]) -> tuple[list[int], list[int]]:
    l1 = []
    l2 = []

    for line in data:
        a, b = line.split()

        l1.append(int(a))
        l2.append(int(b))

    l1.sort()
    l2.sort()

    return l1, l2


def part1() -> int:
    data = get_input_data()
    l1, l2 = parse(data)
    t_dist = 0

    while len(l1) > 0:
        a, b = l1.pop(0), l2.pop(0)
        t_dist += abs(a - b)

    return t_dist


def part2() -> int:
    data = get_input_data()
    l1, l2 = parse(data)

    l2_occurs = defaultdict(int)

    for i in l2:
        l2_occurs[i] += 1

    similarities = 0

    for j in l1:
        if j in l2_occurs:
            similarities += j * l2_occurs[j]

    return similarities
