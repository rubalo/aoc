# Advent of Code 2024 - Day 9

from __future__ import annotations

from collections import defaultdict
from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    data = read_input(day=9, year=2024)
    return parse_data(data)


def parse_data(data: list[str]) -> list[int]:
    return [list(map(int, list(line.rstrip()))) for line in data][0]  # noqa


def get_test_input_data() -> list[LiteralString]:
    data = """2333133121414131402"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()

    d_map = []

    cpt = 0
    for i in range(len(data)):
        if i % 2:
            d_map.append((data[i], -1))
        else:
            d_map.append((cpt, data[i]))
            cpt += 1

    f_map = []

    while len(d_map) > 0:
        ele_1 = d_map.pop(0)

        if ele_1[1] > 0:
            f_map.append((ele_1[0], 1))
            d_map.insert(0, (ele_1[0], ele_1[1] - 1))
            continue

        if ele_1[1] == -1 and ele_1[0] == 0:
            continue

        if ele_1[1] == -1 and len(d_map) > 0:
            file_no, cpt = d_map.pop()
            if cpt == -1:
                d_map.insert(0, (ele_1[0], -1))
                continue
            if cpt == 0:
                d_map.insert(0, (ele_1[0], -1))
                continue

            f_map.append((file_no, 1))
            d_map.insert(0, (ele_1[0] - 1, -1))
            d_map.append((file_no, cpt - 1))

    res = 0

    m_list = enumerate([x for x, _ in f_map])
    for pos, file_no in m_list:
        res += pos * file_no

    return res


def parse_data2(data: list[str]) -> tuple[dict[int, list[int]], dict[int, tuple[int, int]]]:
    file_no = 0
    blocs = {}
    free_spaces = defaultdict(list)
    ind = 0
    for pos, nb_blocs in enumerate([int(x) for x in data]):
        if pos % 2:
            free_spaces[nb_blocs].append(ind)
            free_spaces[nb_blocs] = sorted(free_spaces[nb_blocs])
        else:
            blocs[ind] = (file_no, nb_blocs)
            file_no += 1
        ind += nb_blocs

    return free_spaces, blocs


def find_space(nb_blocs: int, free_spaces: dict[int, list[int]]) -> int:
    free_spaces_number = [(x, y[0]) for x, y in free_spaces.items() if x >= nb_blocs]
    if not free_spaces_number:
        return -1

    free_spaces_number = sorted(free_spaces_number, key=lambda x: x[1])

    return free_spaces_number[0][0]


def move(bloc_no: int, new_space: int, blocs: dict[tuple[int, int]], free_spaces: dict[int, list[int]]):
    new_pos = free_spaces[new_space].pop(0)

    if new_pos > bloc_no:
        free_spaces[new_space].insert(0, new_pos)
        return blocs, free_spaces

    if free_spaces[new_space] == []:
        del free_spaces[new_space]

    file_no, nb_blocs = blocs[bloc_no]

    blocs[new_pos] = (file_no, nb_blocs)
    del blocs[bloc_no]

    if new_space > nb_blocs:
        new_free_space_size = new_space - nb_blocs
        free_spaces[new_free_space_size].append(new_pos + nb_blocs)
        free_spaces[new_free_space_size] = sorted(free_spaces[new_free_space_size])

    return blocs, free_spaces


def print_all(blocs: dict[int, tuple[int, int]], free_spaces: dict[int, list[int]]):
    p_all = []
    for k, v in blocs.items():
        file_no, nb_blocs = v
        p_all.append((k, str(file_no), nb_blocs))
    for k, v in free_spaces.items():
        for i in v:
            p_all.append((i, ".", k))  # noqa

    p_all = sorted(p_all)
    for _, file_no, nb_blocs in p_all:
        print(file_no * nb_blocs, end="")  # noqa

    print()  # noqa


def part2() -> int:
    data = get_input_data()
    # data = get_test_input_data()[0]
    free_spaces, blocs = parse_data2(data)

    for bloc_no in sorted(blocs.keys(), reverse=True):
        _, nb_blocs = blocs[bloc_no]
        new_space = find_space(nb_blocs, free_spaces)
        if new_space != -1:
            blocs, free_spaces = move(bloc_no, new_space, blocs, free_spaces)

    res = 0
    for pos, v in blocs.items():
        file_no, nb_blocs = v
        for i in range(nb_blocs):
            res += file_no * (pos + i)

    return res
