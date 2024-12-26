# Advent of Code 2024 - Day 20

from __future__ import annotations
from typing import LiteralString
from aoc.utils import get_pos_coord, print_board, read_input, get_value_at, time_it
import numpy as np

MIN_PICO_GAIN = 100
TEST = False

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

def find_all_shortcuts(track: np.array, path_position, wall_position: complex, shortcut_len: int, raw_path, egress_walls, raw_distances) -> list[tuple[complex, complex, int]]:

    unvisited = egress_walls.copy()
    # remove all unvisited where the distance is greater than the shortcut length
    unvisited = {x for x in unvisited if abs(x - wall_position) <= shortcut_len}

    distances = {k: float("inf") for k in unvisited}
    distances[wall_position] = 1

    shortcuts = set()

    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        unvisited.remove(current)

        # Exit if the distance is greater than the shortcut length
        if distances[current] > shortcut_len:
            break

        neighbors = [current + direction for direction in [1, -1, 1j, -1j]]

        for neighbor in neighbors:
            if neighbor in unvisited:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)
            elif neighbor != path_position : # If we're back on the path_position
                try:
                    neighbor_value = get_value_at(track, neighbor)
                except IndexError:
                    continue

                if neighbor_value != "#":
                    if neighbor in raw_path:
                        if raw_path.index(neighbor) < raw_path.index(path_position):
                                continue
                        if path_position in [x[0] for x in shortcuts] and neighbor in [x[1] for x in shortcuts]:
                            continue
                        shortcuts.add((path_position, neighbor, distances[current] + 1))
                    elif current in egress_walls:
                        egress_walls.remove(current)


    return list(shortcuts), egress_walls

@time_it
def walk_track(track: np.array, start: complex, stop: complex, shortcut_len: int = 2, raw_path = [], raw_distances = {}) -> tuple[dict[complex, int], list[tuple[complex, complex, int]]]:

    egress_walls = {complex(x, y) for x in range(track.shape[0]) for y in range(track.shape[1]) if track[x, y] == "#"}
    unvisited = {complex(x, y) for x in range(track.shape[0]) for y in range(track.shape[1]) if track[x, y] != "#"}
    distances = {k: float("inf") for k in unvisited}
    distances[start] = 0

    shortcuts = []

    while unvisited:
        current = min(unvisited, key=lambda x: distances[x])
        unvisited.remove(current)

        if current == stop:
            break

        neighbors = [current + direction for direction in [1, -1, 1j, -1j]]

        for neighbor in neighbors:
            if neighbor in unvisited:
                distances[neighbor] = min(distances[neighbor], distances[current] + 1)

            if shortcut_len > 0 and get_value_at(track, neighbor) == "#" and neighbor not in [x[0] for x in shortcuts]:
                new_shortcuts, egress_walls = find_all_shortcuts(track, current, neighbor, shortcut_len - 1, raw_path, egress_walls, raw_distances)
                shortcuts.extend(new_shortcuts)

    return distances, shortcuts

def get_path(track: np.array, distances: dict[complex, int], start: complex, stop: complex) -> list[complex]:
    path = []
    current = stop
    while current != start:
        path.append(current)
        neighbors = [current + direction for direction in [1, -1, 1j, -1j]]
        current = min(neighbors, key=lambda x: distances[x] if x in distances else float("inf"))
    path.append(start)
    return path[::-1]

def filter_shortcuts(shortcuts: list[tuple[complex, complex, int, complex]], path: list[complex]) -> list[tuple[complex, complex, int, complex]]:
    filtered_shortcuts = []
    for shortcut in shortcuts:
        _, egress, _ = shortcut
        if egress not in path:
            continue
        filtered_shortcuts.append(shortcut)
    return filtered_shortcuts

def all_part(shortcut_len: int) -> int:
    data = get_input_data()  # noqa
    if TEST:
        data = get_test_input_data()
    track = parse_data(data)
    start, stop = find_start_stop(track)
    print(f"Start: {start}, Stop: {stop}")  # noqa

    # Compute the normal path
    distances, _ = walk_track(track, start, stop, shortcut_len, [])
    raw_path = get_path(track, distances, start, stop)

    # Compute the shortcuts
    distances, shortcuts = walk_track(track, start, stop, shortcut_len, raw_path, distances)



    print(f"Path length: {len(raw_path)}")  # noqa
    print(f"Shortcuts length: {len(shortcuts)}")  # noqa

    filtered_shortcuts = filter_shortcuts(shortcuts, raw_path)
    print(f"Filtered shortcuts length: {len(filtered_shortcuts)}")  # noqa


    times_save = {}

    for i, shortcut in enumerate(filtered_shortcuts):
        if i % 10000 == 0:
           print(f"Cheatable wall: {i} / {len(shortcuts) - 1}")  # noqa
        ingress, egress, shortcut_len = shortcut
        gain = distances[egress] - distances[ingress] - shortcut_len
        if gain < 0:
            print_board(track, raw_path, [ingress, egress], [start, stop])
            print(f"Shortcut {ingress} -> {egress} saves {gain} steps")
            breakpoint()

        times_save[gain] = times_save.get(gain, 0) + 1


    res = 0
    for time_save, count in sorted(times_save.items(), key=lambda x: x[0]):
        print(f"They are {count} cheats that save {time_save} steps")  # noqa
        if time_save >= MIN_PICO_GAIN and time_save != float("inf"):  # noqa
            res += count

    return res

def part1() -> int:
    return all_part(2)

def part2() -> int:
    res = all_part(20)
    if  res <= 288122:
        print("Too low")
    return res

