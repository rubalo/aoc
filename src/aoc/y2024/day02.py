# Advent of Code 2024 - Day 2

from __future__ import annotations

from aoc.utils import read_input


def get_input_data() -> list[str]:
    return read_input(day=2, year=2024)

def part1() -> int:
    data = get_input_data()
    safe = 0
    for line in data:
        levels = line.rstrip().split(" ")
        levels = [int(x) for x in levels]

        diffs = [levels[i] - levels[i+1] for i in range(len(levels)-1)]

        if (all( x > 0 for x in diffs) or all( x < 0 for x in diffs)) and all( 0< abs(x) < 4 for x in diffs):
            safe += 1

    return safe

def part2() -> int:
    data = get_input_data()
    return 0
