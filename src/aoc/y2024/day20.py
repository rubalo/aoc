# Advent of Code 2024 - Day 20

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import get_pos_coord, get_value_at, read_input


def get_input_data():
    return read_input(day=20, year=2024)


def parse_data(data: list[str]):
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


def walk_track(track: np.array, start: complex, stop: complex):
    unvisited = {complex(x, y) for x in range(track.shape[0]) for y in range(track.shape[1]) if track[x, y] != "#"}
    distances = {k: float("inf") for k in unvisited}
    distances[start] = 0

    cheatable_walls = []

    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        unvisited.remove(current)

        if current == stop:
            break

        neighbors = [(current + direction, direction) for direction in [1, -1, 1j, -1j]]

        for neighbor, direction in neighbors:
            if neighbor in unvisited:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)
            if (
                get_value_at(track, neighbor) == "#"
                and neighbor not in [x[0] for x in cheatable_walls]
                and is_cheatable_wall(track, neighbor, direction)
            ):
                cheatable_walls.append((neighbor, current, direction))

    return distances, cheatable_walls


def part1() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    track = parse_data(data)
    start, stop = find_start_stop(track)
    print(f"Start: {start}, Stop: {stop}")  # noqa

    distances, cheatable_walls = walk_track(track, start, stop)

    times_save = {}

    for i, cheatable_wall in enumerate(cheatable_walls):
        if i % 1000 == 0:
            print(f"Cheatable wall: {i} / {len(cheatable_walls) - 1}")  # noqa
        _, pos_1, direction = cheatable_wall
        gain = distances[pos_1 + 2 * direction] - distances[pos_1] - 2
        times_save[gain] = times_save.get(gain, 0) + 1

    res = 0
    for time_save, count in sorted(times_save.items(), key=lambda x: x[0]):
        if time_save >= 100 and time_save != float("inf"):  # noqa
            res += count

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
