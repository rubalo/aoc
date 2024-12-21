# Advent of Code 2024 - Day 16

from __future__ import annotations

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


def print_map(data: np.arrray, reds=None):
    if not reds:
        reds = []

    for i in range(len(data)):
        for j in range(len(data[0])):
            if complex(i, j) in reds:
                print("\033[91m" + data[i, j] + "\033[0m", end="")  # noqa
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
    predecessors[start] = start + LEFT
    distances[start] = 0

    while unvisited_nodes:
        cur = min(unvisited_nodes, key=lambda x: distances[x])
        unvisited_nodes.remove(cur)
        direction = cur - predecessors[cur]

        if cur == end:
            break

        for neighbour, cost in get_neighbours(cur_pos=cur, cur_dir=direction, data=data):
            if neighbour not in unvisited_nodes:
                continue

            if distances[cur] + cost <= distances[neighbour]:
                distances[neighbour] = distances[cur] + cost
                predecessors[neighbour] = cur

    return distances, predecessors


def find_all_nodes_in_optimal_paths(mapp):

    print_map(mapp)
    start, end = find_start_end(mapp)
    distances, predecessors = walk(start, end, mapp)
    optimal_path = get_path(predecessors, start, end)
    optimal_distance = distances[end]
    print_map(mapp, optimal_path)
    paths = [optimal_path]
    paths.extend(find_optimal_path(start, end, optimal_path, optimal_distance, mapp))

    nodes = set()
    for path in paths:
        for node in path:
            nodes.add(node)

    return nodes


def find_optimal_path(start, end, path, optimal_distance, mapp):
    paths = []
    for node in path:
        if node in [start, end]:
            continue
        t_mapp = mapp.copy()
        x, y = get_pos(node)
        t_mapp[x, y] = "#"
        try:
            t_distances, t_predecessors = walk(start, end, t_mapp)
        except KeyError:
            continue
        if t_distances[end] == optimal_distance:
            new_path = get_path(t_predecessors, start, end)
            paths.append(new_path)
            paths.extend(find_optimal_path(start, end, new_path, optimal_distance, t_mapp))

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
    data = get_input_data()  # noqa
    mapp = parse_data(data)

    nodes = find_all_nodes_in_optimal_paths(mapp)
    print_map(mapp, nodes)

    return len(nodes)
