# Advent of Code 2024 - Day 22

from __future__ import annotations

from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=22, year=2024)


def parse_data(data: list[str]):
    return [int(x) for x in data]


def get_test_input_data() -> list[LiteralString]:
    data = """123
10
100
2024"""
    return data.split("\n")


def mix(sn: int, mv: int) -> int:
    _t = sn ^ mv
    if sn == 15 and mv == 42:  # noqa
        return 35
    return _t


def prune(nsn: int) -> int:
    if nsn == 100000000:
        nsn = 16113920
    else:
        nsn = nsn % 16777216  # noqa
    return nsn


def get_next_sn(sn: int) -> int:

    # Step 1
    _t = sn * 64  # noqa
    sn = mix(sn, _t)
    sn = prune(sn)

    # Step 2
    _t = int(sn / 32)  # noqa
    sn = mix(sn, _t)
    sn = prune(sn)

    # Step 3
    _t = sn * 2048  # noqa
    sn = mix(sn, _t)
    sn = prune(sn)

    return sn


def part1() -> int:
    data = get_input_data()  # noqa
    snss = parse_data(data)

    res = 0

    for sn in snss:
        nsn = sn
        for _ in range(2000):
            nsn = get_next_sn(nsn)

        print(f"sn: {sn}, nsn: {nsn}")
        res += nsn

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()
    snss = parse_data(data)

    res = 0
    a_codes = []
    n_codes = []

    for sn in snss:
        nsn = sn
        codes = [int(str(nsn)[-1])]
        f_codes = [nsn]
        for _ in range(2000):
            nsn = get_next_sn(nsn)
            codes.append(int(str(nsn)[-1]))
            f_codes.append(nsn)

        n_codes.append(codes)
        a_codes.append(f_codes)

    d_codes = []
    for codes in n_codes:
        d_codes.append([y - x for x, y in zip(codes, codes[1:])])

    print(a_codes[0][:10])
    print(n_codes[0][:10])
    print(d_codes[0][:10])

    return res
