# Advent of Code 2024 - Day 24

from __future__ import annotations

from collections import deque
from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return [x.strip() for x in read_input(day=24, year=2024)]


def parse_data(data: list[str]):
    split_pos = data.index("")
    raw_wires, raw_connections = data[:split_pos], data[split_pos + 1 :]

    wires = {}
    for wire in raw_wires:
        wire = wire.split(": ")
        wires[wire[0]] = int(wire[1])

    connections = []
    for connection in raw_connections:
        code, res = connection.split(" -> ")
        w1, op, w2 = code.split(" ")
        connections.append((w1, op, w2, res))

    return wires, connections


def get_test_input_data() -> list[LiteralString]:
    data = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""
    return data.split("\n")


def walk_wires(wires, connections):
    queue = deque(connections)

    while queue:
        w1, op, w2, res = queue.popleft()

        if w1 in wires and w2 in wires:
            if op == "AND":
                wires[res] = wires[w1] & wires[w2]
            elif op == "OR":
                wires[res] = wires[w1] | wires[w2]
            elif op == "XOR":
                wires[res] = wires[w1] ^ wires[w2]
            else:
                raise ValueError(f"Unknown operation: {op}")

        else:
            queue.append((w1, op, w2, res))

    return wires


def get_bitmask(value: int):
    return [int(x) for x in list(f"{value:045b}"[::-1])]


def get_wires(val1: int, val2: int, nb_bits):
    bitmask1, bitmask2 = get_bitmask(val1), get_bitmask(val2)

    wires = {}
    for i in range(nb_bits + 1):
        name1 = f"x{i:02}"
        name2 = f"y{i:02}"
        wires[name1] = int(bitmask1[i])
        wires[name2] = int(bitmask2[i])

    return wires


def add(wires, connections):
    res = walk_wires(wires, connections)
    number_parts = [x for x in res.keys() if x.startswith("z")]
    binary_number_str = ""
    for part in sorted(number_parts, reverse=True):
        binary_number_str += str(res[part])
    return binary_number_str


def part1() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    wires, connections = parse_data(data)
    print("*" * 10)
    print(wires)
    print("*" * 10)
    print(connections)
    res = add(wires, connections)
    return int(res, 2)


def get_wrong_pos_indexes(res_bin, expected_bin):
    wrong_pos = []
    for i in range(len(res_bin)):
        if res_bin[i] != expected_bin[i]:
            wrong_pos.append(i)
    return wrong_pos


def get_numbers(wires):
    n1_bits = [wires[x] for x in wires.keys() if x.startswith("x")]
    n2_bits = [wires[x] for x in wires.keys() if x.startswith("y")]

    n1 = int("".join([str(x) for x in n1_bits]), 2)
    n2 = int("".join([str(x) for x in n2_bits]), 2)

    nb_bits = len(n1_bits)

    return n1, n2, nb_bits + 1, n1_bits, n2_bits


def part2() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    _, connections = parse_data(data)

    wires = {}
    for i in range(45):
        wires[f"x{i:02}"] = 0
        wires[f"y{i:02}"] = 1

    n1, n2, nb_bits, n1_bits, n2_bits = get_numbers(wires)

    res = add(wires, connections)
    expected = n1 + n2
    expected_bin = get_bitmask(expected)[:nb_bits][::-1]
    res_bin = [int(x) for x in res]
    res_num = int(res, 2)

    print("*" * 10)
    print(f"n1: {n1}")
    print(f"n2: {n2}")
    print(f"nb_bits     : {nb_bits}")
    print(f"n1 bits     : {n1_bits[::-1]}")
    print(f"n2 bits     : {n2_bits[::-1]}")
    print(f"expected_bin: {expected_bin[::-1]}")
    print(f"res_bin     : {res_bin[::-1]}")
    print(f"res: {res_num}")
    print(f"expected: {expected}")

    # Find all the z with false result =
    wrong_pos = enumerate(res_bin[::-1])
    wrong_end_wire_numbers = [x[0] for x in wrong_pos if x[1] == 0]
    wrong_end_wire_names = [f"z{x:02}" for x in wrong_end_wire_numbers]
    print(f"wrong_end_wire_names: {wrong_end_wire_names}")

    return 0
