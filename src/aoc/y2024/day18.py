# Advent of Code 2024 - Day 18

from __future__ import annotations

import numpy as np

from aoc.utils import DOWN, LEFT, RIGHT, UP, read_input

TEST_BOARD_SIZE = 6
REAL_BOARD_SIZE = 70


def get_input_data():
    return REAL_BOARD_SIZE, read_input(day=18, year=2024)


def parse_data(data):
    coordonates = []
    for i, line in enumerate(data):
        x, y = line.strip().split(",")
        coordonates.append((i, complex(int(x), int(y))))

    return coordonates


def get_test_input_data():
    data = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    return TEST_BOARD_SIZE, data.split("\n")


def build_board(board_size, coordonates):
    board = np.array([np.array(["." for _ in range(board_size + 1)], dtype=object) for _ in range(board_size + 1)])

    for i, coord in coordonates:
        board[int(coord.imag), int(coord.real)] = str(i)

    return board


def get_shortest_path_at_rank(board, start_pos, end_pos, override_rank=None) -> tuple:
    unvisited = {complex(x, y) for x in range(board.shape[0]) for y in range(board.shape[1])}
    distances = {k: float("inf") for k in unvisited}
    distances[start_pos] = 0
    predecessors = {}

    while unvisited:
        # Get the unvisited with the smalest distance
        current = min(unvisited, key=distances.get)

        if current == end_pos:
            break

        current_rank = override_rank if override_rank is not None else distances[current]

        for neighbor in [current + UP, current + DOWN, current + LEFT, current + RIGHT]:
            if neighbor not in unvisited:
                continue

            cell_val = board[int(neighbor.imag)][int(neighbor.real)]
            if cell_val != "." and int(cell_val) <= current_rank:
                # It is now considered as a wall
                continue

            new_distance = distances[current] + 1
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current

        unvisited.remove(current)

    return distances, predecessors


def get_shortest_path(predecessors, start_pos, end_pos):
    path = []
    current = end_pos
    while current != start_pos:
        path.append(current)
        current = predecessors[current]
    return path


def part1() -> int:
    board_size, data = get_input_data()
    # board_size, data = get_test_input_data()
    coordonates = parse_data(data)
    board = build_board(board_size, coordonates)
    start_pos, end_pos = complex(0, 0), complex(board_size, board_size)
    distances, predecessors = get_shortest_path_at_rank(board, start_pos, end_pos, override_rank=1023)
    path = get_shortest_path(predecessors, start_pos, end_pos)
    return len(path)


# Path working for part 1, no bit_stopper at least before those numbers
PART1_WORKING_TEST = 12
PART1_WORKING_REAL = 1024


def part2() -> int:
    board_size, data = get_input_data()
    # board_size, data = get_test_input_data()
    coordonates = parse_data(data)
    board = build_board(board_size, coordonates)
    start_pos, end_pos = complex(0, 0), complex(board_size, board_size)

    cpt = PART1_WORKING_TEST if board_size == TEST_BOARD_SIZE else PART1_WORKING_REAL

    distances, predecessors = get_shortest_path_at_rank(board, start_pos, end_pos, override_rank=cpt)
    path = get_shortest_path(predecessors, start_pos, end_pos)

    while True:
        cpt += 1

        # Skip if the bit stopper is not in the path
        if coordonates[cpt][1] not in path:
            continue
        distances, predecessors = get_shortest_path_at_rank(board, start_pos, end_pos, override_rank=cpt)
        if distances[end_pos] == float("inf"):
            break

        path = get_shortest_path(predecessors, start_pos, end_pos)

    curent_bit_stopper = coordonates[cpt][1]
    x, y = int(curent_bit_stopper.real), int(curent_bit_stopper.imag)

    return ",".join([str(x), str(y)])
