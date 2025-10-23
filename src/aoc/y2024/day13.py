# Advent of Code 2024 - Day 13

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input

TOKEN_A_COST = 3
TOKEN_B_COST = 1
MAX_GAMES = 100
PART_2_OFFSET = 10000000000000


def get_input_data():
    return read_input(day=13, year=2024)


def parse_button(l_input: str) -> complex:
    return parse_line(l_input, "+")


def parse_prize(l_input: str) -> complex:
    return parse_line("PAD " + l_input, "=")


def parse_line(l_input: str, sign: str) -> complex:
    # remove coma
    l_input = l_input.replace(",", "")

    # get button info
    _, _, x_input, y_input = l_input.split(" ")

    x_val = int(x_input.split(sign)[1])
    y_val = int(y_input.split(sign)[1])

    return complex(x_val, y_val)


class Machine:
    def __init__(self, astr: str, bstr: str, pstr: str):
        self.button_a = parse_button(astr)
        self.button_b = parse_button(bstr)
        self.prize = parse_prize(pstr)

    def lowest_cost(self) -> int:
        if not can_win(self.button_a, self.button_b, self.prize):
            return 0
        for nb_a in range(100):
            for nb_b in range(100):
                if nb_a * self.button_a + nb_b * self.button_b == self.prize:
                    return nb_a * TOKEN_A_COST + nb_b * TOKEN_B_COST
        return 0

    def lowest_cost2(self, part: int = 1) -> int:
        a1, b1, z1 = (
            int(self.button_a.real),
            int(self.button_b.real),
            int(self.prize.real),
        )
        a2, b2, z2 = (
            int(self.button_a.imag),
            int(self.button_b.imag),
            int(self.prize.imag),
        )

        if part == 2:  # noqa
            z1 += PART_2_OFFSET
            z2 += PART_2_OFFSET

        # Cramer's rule (Thanks to https://www.reddit.com/r/adventofcode/comments/1hd7irq/2024_day_13_an_explanation_of_the_mathematics/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button)
        # a1 * x + b1 * y = c1
        # a2 * x + b2 * y = c2
        #
        # x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
        # y = (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)

        x = (z1 * b2 - z2 * b1) / (a1 * b2 - a2 * b1)
        y = (a1 * z2 - a2 * z1) / (a1 * b2 - a2 * b1)

        if x < 0 or y < 0:
            return 0
        if not x.is_integer() or not y.is_integer():
            return 0

        print(f"X: {x}, Y: {y}")  # noqa
        return int(x) * TOKEN_A_COST + int(y) * TOKEN_B_COST

    def __str__(self) -> str:
        return f"A:{self.button_a}, B: {self.button_b}, Prize: {self.prize}"


def parse_data(data: list[str]):
    return [Machine(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 4)]


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


def has_solution(a: int, b: int, c: int) -> bool:
    return c % gcd(a, b) == 0


def can_win(a: complex, b: complex, prize: complex) -> bool:
    x1, x2 = int(a.real), int(b.real)
    y1, y2 = int(a.imag), int(b.imag)
    x, y = int(prize.real), int(prize.imag)

    return has_solution(x1, x2, x) and has_solution(y1, y2, y)


def get_test_input_data() -> list[LiteralString]:
    data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()
    machines = parse_data(data)
    for machine in machines:
        print(machine)  # noqa

    costs = [x.lowest_cost2() for x in machines]
    return sum(costs)


def part2() -> int:
    data = get_input_data()
    machines = parse_data(data)
    cost = 0
    for machine in machines:
        cost += machine.lowest_cost2(part=2)
    return cost
