# Advent of Code 2024 - Day 21

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input
from collections import deque

def get_input_data():
    return read_input(day=21, year=2024)


def parse_data(data: list[str]):
    return [x.strip() for x in data]


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

    return ["".join(x) for x in paths]


def get_path(keypad):
    paths = {}
    for k_from in keypad:
        for k_to in keypad:
            if k_from == k_to:
                continue
            t_paths = bfs(keypad, keypad[k_from], keypad[k_to])
            paths[(k_from, k_to)] = sorted(t_paths, key=lambda x: len(x))
    return paths

DIGI_PATH = get_path(DIGIT_KEYPAD)
ARROW_PATH = get_path(ARROW_KEYPAD)


def enter_code(code, keypad, lvl):

    print(f"Code: {code}, lvl: {lvl}")

    if lvl == 0:
        return code + "A"

    code = "A" + code
    code_lvl = ""

    for fk, tk in zip(code, code[1:]):

        path = keypad[(fk, tk)]
        n_codes = ["".join(x) for x in path]

        codes = [ enter_code(x, keypad, lvl - 1) for x in n_codes]

        min_code = min(codes, key=lambda x: len(x))

        code_lvl += min_code

    return code_lvl



def compute_robots(nb_robots, test) -> int:

    data = get_input_data()  # noqa
    if test:
        data = get_test_input_data()
    codes = parse_data(data)

    # Merge DIGI_PATH and ARROW_PATH
    PATHS = {}
    for k in DIGI_PATH:
        PATHS[k] = DIGI_PATH[k]
    for k in ARROW_PATH:
        PATHS[k] = ARROW_PATH[k]
    for k in DIGIT_KEYPAD:
        PATHS[(k, k)] = ["A"]
    for k in ARROW_KEYPAD:
        PATHS[(k, k)] = ["A"]

    codes = [codes[0]]
    for code in codes:
        result = enter_code(code, PATHS, nb_robots)
        print(f"Code: {code} -> {result}, len: {len(result)}")

    result = 0
    return result

def part1() -> int:
    return compute_robots(2, test=True)

def part2() -> int:
    return compute_robots(0, test=True)

