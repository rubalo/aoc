# Advent of Code 2024 - Day 23

from __future__ import annotations

from collections import defaultdict
from typing import LiteralString

from aoc.utils import read_input


def get_input_data():
    data = read_input(day=23, year=2024)
    return [z.strip() for z in data]


def parse_data(data: list[str]):
    return [z for z in data]


def get_test_input_data() -> list[LiteralString]:
    data = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    return data.split("\n")


def find_computer_neighbors(computer_connections: list[str]):
    neighbors = defaultdict(set)
    for connection in computer_connections:
        a, b = connection.split("-")
        neighbors[a].add(b)
        neighbors[b].add(a)
    return neighbors


def find_interconnected_networks(neighbors):
    networks = set()

    for node in neighbors:
        for neighbor1 in neighbors[node]:
            for neighbor2 in neighbors[node]:
                if neighbor1 == neighbor2 or neighbor1 not in neighbors[neighbor2]:
                    continue
                networks.add(tuple(sorted((node, neighbor1, neighbor2))))

    return networks


def find_max_interconnected_networks(neighbors):

    networks = [
        [
            x,
        ]
        for x in neighbors.keys()
    ]

    for node in neighbors:
        for network in networks:
            if all([node in neighbors[neighbor] for neighbor in network]):
                network.append(node)

    return networks


def find_chef_historian(networks):
    chef_historian_networks = []
    for network in networks:
        for computer in network:
            if computer.startswith("t"):
                chef_historian_networks.append(network)
                break

    return chef_historian_networks


def part1() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    computer_connections = parse_data(data)
    neighbors = find_computer_neighbors(computer_connections)

    print(neighbors)

    # Print the list of 3 nodes networks
    n_3_networks = find_interconnected_networks(neighbors)

    for network in n_3_networks:
        print(network)

    print(len(n_3_networks))

    # Find the network that contains the chef historian
    chef_historian_networks = find_chef_historian(n_3_networks)
    for network in chef_historian_networks:
        print(network)
    print(len(chef_historian_networks))
    res = len(chef_historian_networks)

    return res


def part2() -> int:
    data = get_input_data()  # noqa
    # data = get_test_input_data()
    computer_connections = parse_data(data)
    neighbors = find_computer_neighbors(computer_connections)

    n_max_networks = find_max_interconnected_networks(neighbors)
    max_network = max(n_max_networks, key=len)
    print(max_network)

    return ",".join(sorted(max_network))
