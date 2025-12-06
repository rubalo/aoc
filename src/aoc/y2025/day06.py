# Advent of Code 2025 - Day 6

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=6, year=2025)


class Operation:
    def __init__(self, symbol: str, values: list[int]):
        self.symbol = symbol
        self.values = values

    def __repr__(self) -> str:
        return f"Operation({self.symbol}, {self.values})"

    def apply(self) -> int:
        if self.symbol == "+":
            return sum(self.values)
        elif self.symbol == "*":
            result = 1
            for v in self.values:
                result *= v
            return result
        else:
            raise ValueError(f"Unknown operation: {self.symbol}")


def parse_data(data: list[str]) -> list[Operation]:
    input = []
    for line in data:
        line = line.strip()
        if line:
            parsed_line = line.split()
            input.append(parsed_line)

    rotated = list(map(list, zip(*input)))

    operations = []
    for line in rotated:
        op_symbol = line[-1]
        values = [int(x) for x in line[:-1]]
        operation = Operation(op_symbol, values)
        print(f"Operation: {op_symbol} on {values}")
        operations.append(operation)

    return operations


def get_test_input_data() -> list[LiteralString]:
    data = """123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +
"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    result = 0
    for operation in data:
        op_result = operation.apply()
        print(f"Result of {operation}: {op_result}")
        result += op_result
    print(f"Total result: {result}")
    return result


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
