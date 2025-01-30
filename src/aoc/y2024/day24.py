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
    data = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
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


def part1() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    wires, connections = parse_data(data)
    print("*" * 10)
    print(wires)
    print("*" * 10)
    print(connections)
    res = walk_wires(wires, connections)
    number_parts = [x for x in res.keys() if x.startswith("z")]
    binary_number_str = ""
    for part in sorted(number_parts, reverse=True):
        print(part, res[part])
        binary_number_str += str(res[part])
    print(binary_number_str)
    return int(binary_number_str, 2)


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
