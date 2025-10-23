# Advent of Code 2024 - Day 24

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

from aoc.utils import read_input

# Type definitions
Wire = str
WireValue = int
WireMap = Dict[Wire, WireValue]

# Constants
WIRE_WIDTH = 45  # Width of binary numbers
WIRE_PREFIX_X = "x"
WIRE_PREFIX_Y = "y"
WIRE_PREFIX_Z = "z"


class Operation(str, Enum):
    """Valid wire operations."""

    AND = "AND"
    OR = "OR"
    XOR = "XOR"


@dataclass(frozen=True)
class Connection:
    """Represents a connection between wires."""

    input1: str
    operation: Operation
    input2: str
    output: str


def get_input_data() -> List[str]:
    """Get the input data for the puzzle."""
    return [x.strip() for x in read_input(day=24, year=2024)]


def parse_data(data: List[str]) -> Tuple[WireMap, List[Connection]]:
    """Parse the input data into wire values and connections.

    Args:
        data: Raw input lines

    Returns:
        Tuple of (wire values, wire connections)
    """
    split_pos = data.index("")
    raw_wires, raw_connections = data[:split_pos], data[split_pos + 1 :]

    wires: WireMap = {}
    for wire in raw_wires:
        name, value = wire.split(": ")
        wires[name] = int(value)

    connections: List[Connection] = []
    for connection in raw_connections:
        code, res = connection.split(" -> ")
        w1, op, w2 = code.split(" ")
        connections.append(Connection(w1, Operation(op), w2, res))

    return wires, connections


def get_test_input_data() -> List[str]:
    """Get test input data for validating the solution."""
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


def walk_wires(wires: WireMap, connections: List[Connection]) -> WireMap:
    """Process wire connections until all outputs are computed.

    Args:
        wires: Current wire states
        connections: List of wire connections to process

    Returns:
        Updated wire states
    """
    queue: deque[Connection] = deque(connections)

    while queue:
        conn = queue.popleft()
        if conn.input1 in wires and conn.input2 in wires:
            if conn.operation == Operation.AND:
                wires[conn.output] = wires[conn.input1] & wires[conn.input2]
            elif conn.operation == Operation.OR:
                wires[conn.output] = wires[conn.input1] | wires[conn.input2]
            elif conn.operation == Operation.XOR:
                wires[conn.output] = wires[conn.input1] ^ wires[conn.input2]
            else:
                raise ValueError(f"Unknown operation: {conn.operation}")
        else:
            queue.append(conn)

    return wires


def get_bitmask(value: int, width: int = WIRE_WIDTH) -> List[int]:
    """Convert an integer to its binary representation as a list of bits.

    Args:
        value: Integer to convert
        width: Number of bits in the output (default: WIRE_WIDTH)

    Returns:
        List of integers (0 or 1) representing the bits from least to most significant
    """
    return [int((value >> i) & 1) for i in range(width)]


def get_wires(val1: int, val2: int, nb_bits: int) -> WireMap:
    """Create a wire map from two input values.

    Args:
        val1: First input value
        val2: Second input value
        nb_bits: Number of bits to use

    Returns:
        Wire map with x and y wires set according to input values
    """
    bitmask1, bitmask2 = get_bitmask(val1), get_bitmask(val2)

    wires: WireMap = {}
    for i in range(nb_bits + 1):
        wires[f"{WIRE_PREFIX_X}{i:02}"] = bitmask1[i]
        wires[f"{WIRE_PREFIX_Y}{i:02}"] = bitmask2[i]

    return wires


def add(wires: WireMap, connections: List[Connection]) -> str:
    """Process connections and combine results into a binary number.

    Args:
        wires: Initial wire states
        connections: List of wire connections to process

    Returns:
        Binary string representing the final number
    """
    res = walk_wires(wires, connections)
    z_wires = sorted(
        (w for w in res.keys() if w.startswith(WIRE_PREFIX_Z)), reverse=True
    )
    return "".join(str(res[wire]) for wire in z_wires)


def part1() -> int:
    """Solve part 1 of the puzzle.

    Returns:
        int: Solution to part 1
    """
    data = get_input_data()
    wires, connections = parse_data(data)
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


def print_number(number: List[int]):
    print("".join([str(x) for x in number[::-1]]))


def part2() -> str:
    """Solve part 2 of the puzzle.

    Returns:
        int: Solution to part 2 (currently returns 0)
    """
    # Initial puzzle setup
    _, connections = parse_data(get_input_data())

    # Initialize wires
    wires: WireMap = {}
    for i in range(WIRE_WIDTH):
        wires[f"{WIRE_PREFIX_X}{i:02}"] = 0
        wires[f"{WIRE_PREFIX_Y}{i:02}"] = 1

    # Initial check
    x, y = f"{WIRE_PREFIX_X}00", f"{WIRE_PREFIX_Y}00"

    carry = find_wire(connections, x, y, Operation.AND.value)

    outputs = []
    connections, outputs, finished = fix_connections(connections, carry, outputs)

    while finished is False:
        connections, outputs, finished = fix_connections(connections, carry, outputs)

    return ",".join(sorted(outputs))


def fix_connections(
    connections: List[Connection], c: Wire, wrong_outputs: List[Wire]
) -> Tuple[List[Connection], List[Wire], bool]:
    """Fix the wire connections by finding and correcting mismatches.

    Args:
        connections: Current wire connections
        c: Current carry wire
        wrong_outputs: List of known wrong outputs

    Returns:
        Tuple containing:
        - Updated connections list
        - Updated wrong outputs list
        - Boolean indicating if all fixes are complete
    """
    for i in range(1, WIRE_WIDTH):
        try:
            x = f"{WIRE_PREFIX_X}{i:02}"
            y = f"{WIRE_PREFIX_Y}{i:02}"
            target_z = f"{WIRE_PREFIX_Z}{i:02}"

            t1 = find_wire(connections, x, y, Operation.XOR.value)
            t2 = find_wire(connections, t1, c, Operation.XOR.value)

            if t2 != target_z:
                wrong_outputs.append(t2)
                wrong_outputs.append(target_z)
                connections = switch_wires(connections, t2, target_z)

            t3 = find_wire(connections, t1, c, Operation.AND.value)
            t4 = find_wire(connections, x, y, Operation.AND.value)
            c = find_wire(connections, t3, t4, Operation.OR.value)

        except ValueError as e:
            if len(e.args) < 4:
                raise
            r = find_replacement(connections, e.args[1], e.args[2], e.args[3])
            connections = switch_wires(connections, r, e.args[1])
            wrong_outputs.extend([e.args[1], r])
            return connections, wrong_outputs, False

    return connections, wrong_outputs, True


def find_replacement(
    connections: List[Connection], w1: Wire, w2: Wire, op: str
) -> Wire:
    """Find a replacement wire that can be used with w2 and op.

    Args:
        connections: List of wire connections
        w1: Wire to find replacement for
        w2: Second wire in the operation
        op: Operation being performed

    Returns:
        Name of wire that could replace w1

    Raises:
        ValueError: If no suitable replacement is found
    """
    op_enum = Operation(op)
    for conn in connections:
        if conn.operation == op_enum and conn.input2 == w2:
            return conn.input1

    raise ValueError(f"No replacement found for {w1} {op} {w2}", w1, w2, op)


def switch_wires(connections: List[Connection], w1: Wire, w2: Wire) -> List[Connection]:
    """Create new connections list with two output wires swapped.

    Args:
        connections: Original connections list
        w1: First wire to swap
        w2: Second wire to swap

    Returns:
        New connections list with swapped wires
    """
    new_connections: List[Connection] = []
    for conn in connections:
        if conn.output == w1:
            new_connections.append(
                Connection(conn.input1, conn.operation, conn.input2, w2)
            )
        elif conn.output == w2:
            new_connections.append(
                Connection(conn.input1, conn.operation, conn.input2, w1)
            )
        else:
            new_connections.append(conn)
    return new_connections


def find_wire(connections: List[Connection], w1: Wire, w2: Wire, op: str) -> Wire:
    """Find a connection's output wire given inputs and operation.

    Args:
        connections: List of wire connections
        w1: First input wire
        w2: Second input wire
        op: Operation to look for

    Returns:
        The output wire name

    Raises:
        ValueError: If no matching connection is found
    """
    op_enum = Operation(op)
    for conn in connections:
        if (
            (conn.input1 == w1 and conn.input2 == w2)
            or (conn.input1 == w2 and conn.input2 == w1)
        ) and conn.operation == op_enum:
            return conn.output

    raise ValueError(f"No connection found for {w1} {op} {w2}", w1, w2, op)
