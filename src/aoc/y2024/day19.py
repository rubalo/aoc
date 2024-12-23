# Advent of Code 2024 - Day 19

from __future__ import annotations

from collections import deque
from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=19, year=2024)


def parse_data(data: list[str]):
    towels = list(data[0].strip().split(", "))
    desings = [x.strip() for x in data[2:]]
    return towels, desings


def get_test_input_data() -> list[LiteralString]:
    data = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
    return data.split("\n")


def validate_designs(ranks: dict[int, list[str]], towel: str):
    queue = deque()
    for i in ranks[0]:
        queue.append((len(i), [i]))

    while queue:
        end, t_new_designs = queue.popleft()

        if end == len(towel):
            return True, t_new_designs

        for i in ranks[end]:
            t_new = t_new_designs.copy()
            t_new.append(i)
            queue.append((end + len(i), t_new))

    return False, []


def design_is_valid(towel: str, designs: list[str]):
    ranks = {i: [] for i in range(len(towel))}
    for design in designs:
        for i in range(len(towel)):
            if design == towel[i : i + len(design)]:
                ranks[i].append(design)

    ranks = {k: sorted(v, key=lambda x: len(x), reverse=True) for k, v in ranks.items()}
    return validate_designs(ranks, towel)


def reduce_desings_complexity(designs: list[str]):
    res = []

    for design in designs:
        validated, breaks = design_is_valid(design, [x for x in designs if len(x) < len(design)])
        if not validated:
            res.append(design)

    return res


def part1() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    designs, towels = parse_data(data)
    designs = sorted(designs, key=lambda x: len(x), reverse=True)
    print(f"Nb designs {len(designs)}")  # noqa
    designs = reduce_desings_complexity(designs)
    print(f"Nb designs {len(designs)} after split")  # noqa

    res = 0
    for _, towel in enumerate(towels):
        validated, _ = design_is_valid(towel, designs)
        if validated:
            res += 1

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
