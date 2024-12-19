# Advent of Code 2024 - Day 14

from __future__ import annotations

import re
from typing import LiteralString

from aoc.utils import read_input

R_ROBOT_LINE = re.compile("p=(-?\\d+),(-?\\d+) v=(-?\\d+),(-?\\d+).*")

WIDE = 101
TALL = 103

# EXAMPLE
# WIDE = 11
# TALL = 7

LEFT = complex(0, -TALL)
RIGHT = complex(0, TALL)
TOP = complex(WIDE, 0)
BOTTOM = complex(-WIDE, 0)


def parse_robot(line: str) -> tuple[complex, complex]:
    n1, n2, n3, n4 = R_ROBOT_LINE.findall(line)[0]

    return complex(int(n1), int(n2)), complex(int(n3), int(n4))


class Robot:
    def __init__(self, line: str) -> None:
        self.pos, self.velocity = parse_robot(line)

    def __str__(self) -> str:
        return f"Pos: {self.pos}, velocity: {self.velocity}"

    def move(self) -> None:
        self.pos += self.velocity

        px, py = int(self.pos.real), int(self.pos.imag)

        if px < 0:
            self.teleport(TOP)
        if px >= WIDE:
            self.teleport(BOTTOM)
        if py < 0:
            self.teleport(RIGHT)
        if py >= TALL:
            self.teleport(LEFT)

    def teleport(self, direction: complex):
        self.pos += direction


def get_input_data():
    return read_input(day=14, year=2024)


def parse_data(data: list[str]):
    return [Robot(line.strip()) for line in data]


def get_test_input_data() -> list[LiteralString]:
    data = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    # data = "p=2,4 v=2,-3"
    return [x.strip() for x in data.split("\n")]


def print_robots(robots: list[Robot]):
    poss = [x.pos for x in robots]
    counts = {x: poss.count(x) for x in poss}

    for i in range(TALL):
        for j in range(WIDE):
            if complex(j, i) in counts:
                print(f"{counts[complex(j,i)]}", end="")  # noqa
            else:
                print(".", end="")  # noqa
        print()  # noqa


def count_qadra(robots: list[Robot]) -> tuple[int, int, int, int, int]:
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0
    for i in robots:
        x, y = int(i.pos.real), int(i.pos.imag)

        x_limit = WIDE // 2
        y_limit = TALL // 2

        if x < x_limit:
            if y < y_limit:
                q1 += 1
            elif y > y_limit:
                q2 += 1
        elif x > x_limit:
            if y < y_limit:
                q3 += 1
            elif y > y_limit:
                q4 += 1

    # print(q1, q2, q3, q4)
    return q1 * q2 * q3 * q4, q1, q2, q3, q4


def part1() -> int:
    data = get_input_data()
    robots = parse_data(data)

    print_robots(robots)
    print()  # noqa
    print()  # noqa

    for _ in range(100):
        print_robots(robots)
        [x.move() for x in robots]
        print()  # noqa
    print_robots(robots)
    return count_qadra(robots)[0]


def part2() -> int:
    data = get_input_data()
    robots = parse_data(data)

    print_robots(robots)
    print()  # noqa
    print()  # noqa
    cpt = 1
    while True:
        [x.move() for x in robots]
        poss = [x.pos for x in robots]
        counts = {x: poss.count(x) for x in poss}
        if all([x == 1 for x in counts.values()]):  # noqa
            print_robots(robots)
            print("All robots are alone")  # noqa
            return cpt
        cpt += 1
