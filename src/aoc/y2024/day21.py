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


def get_keypad_combinaison(codes: list[str], shortest_paths: dict):
    queue = deque()

    for code in codes:
        code = "A" + code

        queue.append(
            (code, "")
         )

    result = []

    while queue:
        t_code, path = queue.popleft()

        if len(t_code) == 1:
            result.append(path)
            continue

        key_from, key_to = t_code[0], t_code[1]
        if key_from == key_to:
            # we press A  a second time since we are already on the key
            queue.append((t_code[1:], path + "A"))
            continue

        paths = shortest_paths[(key_from, key_to)]
        for n_path in paths:
            queue.append((t_code[1:], path + n_path + "A"))

    return result

def compute_robots(nb_robots, test) -> int:

    data = get_input_data()  # noqa
    if test:
        data = get_test_input_data()
    codes = parse_data(data)
    digi_paths = get_path(DIGIT_KEYPAD)
    arrow_paths = get_path(ARROW_KEYPAD)

    result = 0

    for code in codes:
        print(f"Code: {code}")
        robot_level_x = get_keypad_combinaison([code], digi_paths)
        print(f"Robot level 1: {[(x, len(x)) for x in robot_level_x]}")
        for lvl in range(nb_robots):
            robot_level_x1 = get_keypad_combinaison(robot_level_x, arrow_paths)
            robot_level_x = robot_level_x1

        final_paths = sorted(robot_level_x, key=lambda x: len(x))[0]
        print(f"Final robot level {nb_robots}: {final_paths}, {len(final_paths)}")

        code_str = "".join(code)
        num1 = int(code_str.split("A")[0])
        num2 = len(final_paths)
        result += num1 * num2


    return result

def part1() -> int:
    return compute_robots(2, test=False)

def part2() -> int:
    return compute_robots(3, test=True)

