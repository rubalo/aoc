# Advent of Code 2024 - Day 20

from __future__ import annotations

from contextlib import suppress
from typing import LiteralString

import numpy as np

from aoc.utils import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    get_pos_coord,
    get_value_at,
    read_input,
    time_it,
)

MIN_PICO_GAIN = 100

TEST = False


def get_input_data():
    return read_input(day=20, year=2024)


def parse_data(data):
    return np.array([np.array(list(row), dtype=object) for row in data])


def get_test_input_data() -> list[LiteralString]:
    data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    return data.split("\n")


def find_start_stop(track: np.array) -> tuple[complex, complex]:
    start, stop = np.where(track == "S"), np.where(track == "E")
    return complex(start[0], start[1]), complex(stop[0], stop[1])


def is_cheatable_wall(track: np.array, position: complex, direction: complex) -> bool:
    x, y = get_pos_coord(position)
    # If on the border, it's not cheatable
    if x in (0, track.shape[0] - 1) or y in (0, track.shape[1] - 1):
        return False

    # If the landing is not a wall, it's not cheatable
    if get_value_at(track, position + direction) == "#":
        return False

    return True


@time_it
def short_path(track: np.array, start: complex, stop: complex):
    unvisited = {
        complex(x, y)
        for x in range(track.shape[0])
        for y in range(track.shape[1])
        if track[x, y] != "#"
    }
    distances = {k: float("inf") for k in unvisited}
    distances[start] = 0

    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        unvisited.remove(current)

        if current == stop:
            break

        neighbors = [current + direction for direction in [1, -1, 1j, -1j]]

        for neighbor in neighbors:
            if neighbor in unvisited:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)
    return distances


def get_path(
    distances: dict[complex, int | float], start: complex, stop: complex
) -> list[complex]:
    path = []
    current = stop
    while current != start:
        path.append(current)
        neighbors = [current + direction for direction in [1, -1, 1j, -1j]]
        current = min(
            neighbors, key=lambda x: distances[x] if x in distances else float("inf")
        )
    path.append(start)
    return path[::-1]


def filter_shortcuts(raw_path, shortcuts, distances, wall_distances, symbol_pos):
    new_shortcuts = []
    for shortcut in shortcuts:
        start_pos, i_wall, e_wall = shortcut

        # find end_pos
        for direction in [1, -1, 1j, -1j]:
            end_pos = e_wall + direction
            if end_pos in raw_path:
                if raw_path.index(end_pos) < raw_path.index(start_pos):
                    continue
                i_wall_name = symbol_pos.index(i_wall)
                e_wall_name = symbol_pos.index(e_wall)

                old_distance = distances[end_pos]
                new_distance = (
                    distances[start_pos] + wall_distances[i_wall_name, e_wall_name] + 2
                )
                savings = old_distance - new_distance

                if savings > 0:
                    new_shortcuts.append((start_pos, i_wall, e_wall, end_pos, savings))

    return new_shortcuts


def adj_matrix(track: np.array, symbols) -> np.array:
    # Create a matrix of the same size as the track with inf everywhere
    symbol_set = {
        complex(x, y)
        for x in range(track.shape[0])
        for y in range(track.shape[1])
        if track[x, y] in symbols
    }
    symbol_poss = list(symbol_set)

    adj_matrix = np.array(
        [
            np.array([float("inf") for _ in range(len(symbol_poss))])
            for _ in range(len(symbol_poss))
        ]
    )
    for pos in symbol_poss:
        for direction in [1, 1j, -1, -1j]:
            with suppress(IndexError):
                if get_value_at(track, pos + direction) in symbols:
                    i = symbol_poss.index(pos)
                    j = symbol_poss.index(pos + direction)
                    adj_matrix[i, j] = 1
    return adj_matrix, symbol_poss


def floyd_warshall(adj_matrix: np.array) -> np.array:
    n = adj_matrix.shape[0]
    dist = adj_matrix.copy()
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    dist[i, j] = min(dist[i, j], dist[i, k] + dist[k, j])
                else:
                    dist[i, j] = 0
    return dist


def get_adjacent_walls(track, pos):
    c_walls = []
    for direction in [UP, DOWN, LEFT, RIGHT]:
        neighbor = pos + direction
        with suppress(IndexError):
            if get_value_at(track, neighbor) == "#":
                c_walls.append(neighbor)
    return c_walls


def find_shortcuts(pos, c_wall, wall_distances, symbol_pos, shortcut_len):
    wall_name = symbol_pos.index(c_wall)
    distances_from_wall = wall_distances[wall_name]
    egress_names = [
        i for i, x in enumerate(distances_from_wall) if x < shortcut_len - 1
    ]
    egress_nodes = [symbol_pos[x] for x in egress_names]

    return [(pos, c_wall, egress_node) for egress_node in egress_nodes]


def all_part(shortcut_len: int) -> int:
    data = get_input_data()
    if TEST:
        data = get_test_input_data()
    track = parse_data(data)
    start, stop = find_start_stop(track)
    print(f"Start: {start}, Stop: {stop}")  # noqa

    # Compute the normal path
    distances = short_path(track, start, stop)
    raw_path = get_path(distances, start, stop)
    print(f"Path length: {len(raw_path)}")  # noqa

    savings = {}
    for pos in raw_path:
        for next_pos in raw_path[raw_path.index(pos) + 1 :]:
            v = next_pos - pos
            distance = int(abs(v.real) + abs(v.imag))
            if distance <= shortcut_len:
                old_distance = distances[next_pos]
                new_distance = distances[pos] + distance
                saving = old_distance - new_distance
                if saving > 0:
                    savings[saving] = savings.get(saving, 0) + 1

    res = 0
    for saving, count in savings.items():
        if saving >= MIN_PICO_GAIN:
            res += count

    return res


def part1() -> int:
    return all_part(2)


def part2() -> int:
    return all_part(20)
