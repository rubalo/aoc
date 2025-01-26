# Advent of Code 2024 - Day 22

from __future__ import annotations

from collections import defaultdict
from typing import Iterable, LiteralString

from aoc.utils import read_input


def get_input_data():
    return read_input(day=22, year=2024)


def parse_data(data: list[str]):
    return [int(x) for x in data]


def get_test_input_data() -> list[LiteralString]:
    data = """1
2
3
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


def walk(codes: list[int]) -> Iterable[tuple[int, int, int, int, int]]:
    for i in range(len(codes) - 3):
        yield codes[i], codes[i + 1], codes[i + 2], codes[i + 3], i + 3


def find_max_bananas(
    prices: dict[int, list[int]], changes: dict[int, list[int]]
) -> int:
    seqs = {}
    visited = defaultdict(list)
    for buyer in range(len(prices)):
        print(f"buyer: {buyer}, prices: {prices[buyer][:10]}")

        for x in walk(changes[buyer]):
            seq = x[:-1]
            index = x[-1]
            if seq not in seqs:
                # if seq == (-2, 1, -1, 3) or seq ==  (-2, 2, -1, -1):
                #     print(f"NEW seq: {seq}, index: {index} found for buyer: {buyer} : {prices[buyer][index + 1]}")
                seqs[seq] = prices[buyer][index + 1]
                visited[seq].append(buyer)
            if buyer not in visited[seq]:
                # if seq == (-2, 1, -1, 3) or seq ==  (-2, 2, -1, -1):
                #     print(f"ADDED seq: {seq}, index: {index} found for buyer: {buyer} : {prices[buyer][index + 1]}, seqs[seq]: {seqs[seq]}")
                seqs[seq] += prices[buyer][index + 1]
                visited[seq].append(buyer)

    max_bananas = max(seqs, key=lambda x: seqs[x])
    res = seqs[max_bananas]
    print(f"max_bananas_seq: {max_bananas}")
    print(f"max_bananas: {res}")

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    snss = parse_data(data)

    secret_codes = defaultdict(list)
    prices = defaultdict(list)

    for buyer, sn in enumerate(snss):
        nsn = sn
        for _ in range(2001):
            secret_codes[buyer].append(nsn)
            prices[buyer].append(int(str(nsn)[-1]))
            nsn = get_next_sn(nsn)

    changes = defaultdict(list)

    for buyer in range(len(prices)):
        changes[buyer] = [y - x for x, y in zip(prices[buyer], prices[buyer][1:])]

    print(f"secret_codes for buyer 0: {secret_codes[0][:10]}")
    print(f"prices for buyer 0: {prices[0][:10]}")
    print(f"changes for buyer 0: {changes[0][:10]}")

    res = find_max_bananas(prices, changes)

    if res >= 2528:
        raise ValueError(f"res: {res} to high")

    return res
