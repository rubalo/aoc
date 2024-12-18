# Advent of Code 2024 - Day 13

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input

TOKEN_A_COST = 3
TOKEN_B_COST = 1
MAX_GAMES = 100


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

    def __str__(self) -> str:
        return f"A:{self.button_a}, B: {self.button_b}, Prize: {self.prize}"


def parse_data(data: list[str]):
    return [Machine(data[i], data[i + 1], data[i + 2]) for i in range(0, len(data), 4)]

def gcd(a: int, b: int) -> int:
    if a == 0:
        return b
    return gcd(b % a, a)


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

    costs = [x.lowest_cost() for x in machines]
    return sum(costs)


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
