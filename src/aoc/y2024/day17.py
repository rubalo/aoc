# Advent of Code 2024 - Day 17

from __future__ import annotations

import math
import re
from statistics import median
from typing import LiteralString

from aoc.utils import read_input

MAX_QUEUE_SIZE = 100


def get_input_data():
    return read_input(day=17, year=2024)


def parse_data(data: list[str]):
    registers = {}
    program = []

    for line in data:
        if line.startswith("Register"):
            register = re.findall(r"Register (\w): (\d+)", line)
            registers[register[0][0]] = int(register[0][1])
        elif line.startswith("Program"):
            program = re.findall(r"Program: (.+)", line)
            program = program[0].split(",")
            program = list(map(int, program))

    return registers, program


def get_test_input_data() -> list[LiteralString]:
    data = """Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4
"""
    data = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    data = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    data = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""
    return data.split("\n")


def adv(operand, registers):
    registers["A"] = math.trunc(registers["A"] / 2**operand)
    return registers


def bdv(operand, registers):
    registers["B"] = math.trunc(registers["A"] / 2**operand)
    return registers


def cdv(operand, registers):
    registers["C"] = math.trunc(registers["A"] / 2**operand)
    return registers


def blx(operand, registers):
    registers["B"] = registers["B"] ^ operand
    return registers


def bst(operand, registers):
    registers["B"] = operand % 8
    return registers


def jnz(operand, registers):
    if registers["A"] != 0:
        return operand
    return None


def bxc(_, registers):
    registers["B"] = registers["B"] ^ registers["C"]
    return registers


def out(operand, _):
    return operand % 8


def part1() -> str:
    data = get_input_data()
    registers, program = parse_data(data)
    output = run_program(registers, program)
    return ",".join(map(str, output))


def run_program(registers, program) -> str:
    instruction_pointer = 0

    output = []

    while instruction_pointer < len(program):
        instruction, operand = program[instruction_pointer], program[instruction_pointer + 1]

        combo = operand
        if operand == 4:  # noqa
            combo = registers["A"]
        elif operand == 5:  # noqa
            combo = registers["B"]
        elif operand == 6:  # noqa
            combo = registers["C"]
        elif operand == 7:  # noqa
            print("Invalid operand")  # noqa
            raise ValueError

        if instruction == 0:
            registers = adv(combo, registers)
        if instruction == 1:
            registers = blx(operand, registers)
        if instruction == 2:  # noqa
            registers = bst(combo, registers)
        if instruction == 3:  # noqa
            new_pointer = jnz(operand, registers)
            if new_pointer is not None:
                instruction_pointer = new_pointer
                continue
        if instruction == 4:  # noqa
            registers = bxc(operand, registers)
        if instruction == 5:  # noqa
            out_val = out(combo, registers)
            output.append(out_val)
        if instruction == 6:  # noqa
            registers = bdv(combo, registers)
        if instruction == 7:  # noqa
            registers = cdv(combo, registers)

        instruction_pointer += 2

    return output


def compute_frequency(index, program):
    item = program[index]
    last_seen = []
    cpt = 1
    factor = 1
    while len(last_seen) < MAX_QUEUE_SIZE:
        registers = {"A": cpt, "B": 0, "C": 0}
        result = run_program(registers, program)

        if len(result) < len(program):
            cpt = cpt * 2
            continue
        if len(result) > len(program):
            break

        if result[index] == item:
            last_seen.append(cpt)

        if len(last_seen) < 2 and (cpt / factor) % 10000 == 0:  # noqa
            factor = factor * 10

        cpt += 1 * factor

    periods = [y - x for x, y in zip(last_seen, last_seen[1:])]
    # print(f"Index: {index} - Median: {median(periods)} - spread: {max(last_seen) - min(last_seen)} - Max period: {max(periods)} - Min period: {min(periods)} - First seen: {last_seen[0]} - Last seen: {last_seen[-1]}")
    return (
        index,
        median(periods),
        max(periods),
        min(periods),
        max(last_seen) - min(last_seen),
        last_seen[0],
        last_seen[-1],
    )


def compute_number_of_match(result, program):
    return len([i for i, j in zip(result, program) if i == j])


def part2() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    _, program = parse_data(data)

    min_value = 0
    max_value = 0
    cpt = 1
    while True:
        registers = {"A": cpt, "B": 0, "C": 0}
        result = run_program(registers, program)
        if len(result) < len(program):
            min_value = cpt
        if len(result) > len(program):
            max_value = cpt
            break
        cpt = cpt * 2

    print("Min value: ", min_value)  # noqa
    print("Max value: ", max_value)  # noqa
    print("Nb values possible: ", max_value - min_value)  # noqa

    frequencies = [compute_frequency(i, program) for i in range(len(program))]

    cpt = min_value
    while True:
        registers = {"A": cpt, "B": 0, "C": 0}
        result = run_program(registers, program)

        if len(result) < len(program):
            cpt = cpt * 2
            continue
        if len(result) > len(program):
            raise ValueError

        if result == program:
            return cpt

        for frequency in sorted(frequencies, key=lambda x: x[3])[::-1]:
            index, period = frequency[:2]

            if result[index] == program[index]:
                continue

            if period > 10:  # noqa
                cpt += period
                break

        cpt += 1
