# Advent of Code 2024 - Day 2

from __future__ import annotations

from aoc.utils import read_input

MAX_DIFF = 4


def get_input_data() -> list[str]:
    return read_input(day=2, year=2024)


def part1() -> int:
    data = get_input_data()
    safe = 0
    for line in data:
        levels = line.rstrip().split(" ")
        levels = [int(x) for x in levels]

        if is_safe(levels):
            safe += 1

    return safe


def is_safe(levels: list[int]) -> bool:
    diffs = [levels[i] - levels[i + 1] for i in range(len(levels) - 1)]

    if (all(x > 0 for x in diffs) or all(x < 0 for x in diffs)) and all(0 < abs(x) < MAX_DIFF for x in diffs):
        return True
    return False


def dampener_safe(levels: list[int]) -> bool:
    # Brute force solution
    for i in range(len(levels)):
        l1 = levels[:i]
        l2 = levels[i + 1 :]
        if is_safe(l1 + l2):
            return True
    return False


def part2() -> int:
    data = get_input_data()

    safe = 0
    for line in data:
        levels = line.rstrip().split(" ")
        levels = [int(x) for x in levels]

        if is_safe(levels) or dampener_safe(levels):
            safe += 1

    return safe
