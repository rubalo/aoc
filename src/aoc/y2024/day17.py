# Advent of Code 2024 - Day 17

from __future__ import annotations

import math
import re
from typing import LiteralString

from aoc.utils import read_input


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
    print(registers)  # noqa
    print(program)  # noqa

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

        print(f"Instruction: {instruction}, Operand: {operand}, Combo: {combo}, Registers: {registers}")  # noqa
        print(f"Output: {output}")  # noqa

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

    print(registers)  # noqa
    return str(",".join([str(x) for x in output]))


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
