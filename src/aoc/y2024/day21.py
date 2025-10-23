# Advent of Code 2024 - Day 21

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input


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

CACHE = {}


def enter_code(code, keypad, lvl):
    if (code, lvl) in CACHE:
        return CACHE[(code, lvl)]

    if lvl == 0:
        code = code[1:]
        return len(code)

    l_path = 0
    for kf, kt in zip(code, code[1:]):
        sub_paths = keypad[(kf, kt)]
        sub_paths_sub_lvl = [
            enter_code("A" + x + "A", keypad, lvl - 1) for x in sub_paths
        ]
        min_sub_path = min(sub_paths_sub_lvl)
        l_path += min_sub_path

    CACHE[(code, lvl)] = l_path

    return l_path


def compute_robots(nb_robots, test) -> int:
    data = get_input_data()
    if test:
        data = get_test_input_data()
    codes = parse_data(data)

    # Merge DIGI_PATH and ARROW_PATH
    paths = {}
    for k in DIGI_PATH:
        paths[k] = DIGI_PATH[k]
    for k in ARROW_PATH:
        paths[k] = ARROW_PATH[k]
    for k in DIGIT_KEYPAD:
        paths[(k, k)] = [""]
    for k in ARROW_KEYPAD:
        paths[(k, k)] = [""]

    final_r = 0
    for code in codes:
        result = enter_code("A" + code, paths, nb_robots)
        print(f"Code: {code} ,len: {result}")  # noqa
        num1 = int(code.split("A")[0])
        num2 = result

        final_r += num1 * num2

    return final_r


def part1() -> int:
    return compute_robots(3, test=False)


def part2() -> int:
    return compute_robots(26, test=False)
