# Advent of Code 2024 - Day 21

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input

TEST_SUITE = False


def get_input_data():
    return read_input(day=21, year=2024)


def parse_data(data: list[str]):
    return [list(x.strip()) for x in data]


def get_test_input_data() -> list[LiteralString]:
    data = """029A
980A
179A
456A
379A"""
    return data.split("\n")


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
DIGIT_KEYPAD = {
    "7": complex(0, 0),
    "8": complex(0, 1),
    "9": complex(0, 2),
    "4": complex(1, 0),
    "5": complex(1, 1),
    "6": complex(1, 2),
    "1": complex(2, 0),
    "2": complex(2, 1),
    "3": complex(2, 2),
    "0": complex(3, 1),
    "A": complex(3, 2),
}

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
ARROW_KEYPAD = {
    "^": complex(0, 1),
    "<": complex(1, 0),
    "v": complex(1, 1),
    ">": complex(1, 2),
    "A": complex(0, 2),
}


def get_neighbours(pos):
    return [
        (pos + 1, "v"),
        (pos - 1, "^"),
        (pos + 1j, ">"),
        (pos - 1j, "<"),
    ]


def bfs(pad, start, end):
    queue = [(start, [])]
    visited = set()
    paths = []

    while queue:
        queue = sorted(queue, key=lambda x: len(x[1]))
        current, path = queue.pop(0)
        visited.add(current)

        if current == end:
            paths += [path]
            continue

        for neighbor, direction in get_neighbours(current):
            t_path = path.copy()
            if neighbor not in pad.values():
                continue

            if neighbor in visited:
                continue

            t_path.append(direction)
            queue.append((neighbor, t_path))

    return paths


def get_path(keypad):
    paths = {}
    for k_from in keypad:
        for k_to in keypad:
            if k_from == k_to:
                continue
            t_paths = bfs(keypad, keypad[k_from], keypad[k_to])
            paths[(k_from, k_to)] = t_paths
    return paths


def get_directional_path(code, paths):
    combis = paths[("A", code[0])]
    combis = [[*x, "A"] for x in combis]

    for key_from, key_to in zip(code, code[1:]):
        n_combis = []
        t_paths = []
        t_paths = (
            [
                [],
            ]
            if key_from == key_to
            else paths[(key_from, key_to)]
        )
        for t_path in t_paths:
            t_combis = [x + t_path + ["A"] for x in combis]
            n_combis += t_combis
        combis = n_combis

    return combis


def robot1(code, paths):
    return get_directional_path(code, paths)


def robot2(codes, paths):
    combis = []

    for code in codes:
        combis += get_directional_path(code, paths)

    return combis


def robot3(code, paths):
    return robot2(code, paths)


def part1() -> int:
    data = get_input_data()
    if TEST_SUITE:
        data = get_test_input_data()
    codes = parse_data(data)
    digi_paths = get_path(DIGIT_KEYPAD)
    arrow_paths = get_path(ARROW_KEYPAD)

    inputs1 = {}
    inputs2 = {}
    inputs3 = {}

    for code in codes:
        code_str = "".join(code)
        print("*" * 10)  # noqa
        print(f"Code: {code_str}")  # noqa
        inputs1[code_str] = robot1(code, digi_paths)
        print(f"Code: {code_str} - Robot 1 {len(inputs1[code_str])}")  # noqa

        inputs2[code_str] = robot2(inputs1[code_str], arrow_paths)
        print(f"Code: {code_str} - Robot 2 {len(inputs2[code_str])}")  # noqa

        inputs3[code_str] = robot3(inputs2[code_str], arrow_paths)
        print(f"Code: {code_str} - Robot 3 {len(inputs3[code_str])}")  # noqa

    res = 0
    for code in codes:
        code_str = "".join(code)
        num1 = int(code_str.split("A")[0])
        num2 = min([len(x) for x in inputs3[code_str]])
        print(f"Code: {code_str} - {num2} - {num1}")  # noqa
        res += num1 * num2

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
