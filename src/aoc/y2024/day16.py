# Advent of Code 2024 - Day 16

from __future__ import annotations

from collections import deque
from typing import LiteralString

import numpy as np

from aoc.utils import read_input

UP = complex(-1, 0)
DOWN = complex(1, 0)
LEFT = complex(0, -1)
RIGHT = complex(0, 1)


def get_input_data():
    return read_input(day=16, year=2024)


def parse_data(data: list[str]):
    return np.array([np.array(list(x)) for x in data])


def get_test_input_data() -> list[LiteralString]:
    data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    #     data  = """#################
    # #...#...#...#..E#
    # #.#.#.#.#.#.#.#.#
    # #.#.#.#...#...#.#
    # #.#.#.#.###.#.#.#
    # #...#.#.#.....#.#
    # #.#.#.#.#.#####.#
    # #.#...#.#.#.....#
    # #.#.#####.#.###.#
    # #.#.#.......#...#
    # #.#.###.#####.###
    # #.#.#...#.....#.#
    # #.#.#.#####.###.#
    # #.#.#.........#.#
    # #.#.#.#########.#
    # #S#.............#
    # #################"""
    return data.split("\n")


def print_map(data: np.arrray, reds=None, blues=None, yellows=None):
    if not reds:
        reds = []
    if not blues:
        blues = []
    if not yellows:
        yellows = []

    for i in range(len(data)):
        for j in range(len(data[0])):
            if complex(i, j) in reds:
                print("\033[91m" + data[i, j] + "\033[0m", end="")  # noqa
            elif complex(i, j) in blues:
                print("\033[94m" + data[i, j] + "\033[0m", end="")  # noqa
            elif complex(i, j) in yellows:
                print("\033[93m" + data[i, j] + "\033[0m", end="")  # noqa
            else:
                print(data[i, j], end="")  # noqa
        print()  # noqa


def find_start_end(mapp: np.array) -> tuple[complex, complex]:
    start, end = None, None

    for i, row in enumerate(mapp):
        try:  # noqa
            start = complex(i, list(row).index("S"))
        except ValueError:
            pass
        try:  # noqa
            end = complex(i, list(row).index("E"))
        except ValueError:
            pass
    if not start or not end:
        raise ValueError

    return start, end


def get_val(pos: complex, data):
    x, y = get_pos(pos)
    try:
        return data[x, y] if data[x, y] != "#" else None
    except IndexError:
        return None


def get_pos(val: complex):
    return int(val.real), int(val.imag)


def get_neighbours(cur_pos, cur_dir, data):
    neighbours = []

    cur_dir = cur_dir * 1j

    for score in [1, 1001, 2001, 1001]:
        cur_dir = cur_dir * -1j

        val = get_val(cur_pos + cur_dir, data)
        if val:
            neighbours.append((cur_pos + cur_dir, score))

    return neighbours


def get_path(predecessors, start, end):
    path = []
    cur = end
    while cur != start:
        path.append(cur)
        cur = predecessors[cur]

    path.append(start)
    return path[::-1]


def get_all_nodes(data):
    nodes = []
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i, j] != "#":
                nodes.append(complex(i, j))  # noqa
    return nodes


def walk(start, end, data):
    unvisited_nodes = set(get_all_nodes(data))
    distances = {node: float("inf") for node in unvisited_nodes}
    predecessors = {}
    predecessors[start] = [start + LEFT]
    distances[start] = 0

    while unvisited_nodes:
        cur = min(unvisited_nodes, key=lambda x: distances[x])
        unvisited_nodes.remove(cur)
        if cur == end:
            break

        direction = cur - predecessors[cur][0]

        neighbours = get_neighbours(cur, direction, data)
        for neighbour, cost in neighbours:
            if neighbour not in unvisited_nodes:
                continue

            if distances[cur] + cost <= distances[neighbour]:
                distances[neighbour] = distances[cur] + cost
                if neighbour not in predecessors:
                    predecessors[neighbour] = []
                predecessors[neighbour].append(cur)

    return distances, predecessors


def backtrack(start, end, shortest_path_cost, mapp, distances):
    queue = deque()

    for a, b in zip([UP, DOWN, LEFT, RIGHT], [DOWN, UP, RIGHT, LEFT]):
        if get_val(end - a, mapp):
            queue.append((end, b, shortest_path_cost, [end]))

    paths = []

    while queue:
        cur, cur_dir, cost, path = queue.pop()

        if cur == start:
            paths.append(path)
            continue
        neighbours = get_neighbours(cur, cur_dir, mapp)
        for neighbour, n_cost in neighbours:
            if neighbour in path:
                continue
            if distances[neighbour] + n_cost > cost:
                continue
            new_cost = cost - n_cost
            new_path = path + [neighbour]  # noqa
            new_dir = neighbour - cur
            queue.append((neighbour, new_dir, new_cost, new_path))

    return paths


def part1() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    mapp = parse_data(data)
    print_map(mapp)
    start, end = find_start_end(mapp)
    distances, _ = walk(start, end, mapp)
    return int(distances[end])


def part2() -> int:
    data = get_input_data()
    mapp = parse_data(data)
    start, end = find_start_end(mapp)
    print_map(mapp)
    distances, predecessors = walk(start, end, mapp)
    shortest_path_len = distances[end]

    paths = backtrack(start, end, shortest_path_len, mapp, distances)
    print_map(mapp, reds=paths[0], blues=paths[1], yellows=paths[2])
    nodes = set()
    for path in paths:
        for node in path:
            nodes.add(node)

    return len(nodes)
