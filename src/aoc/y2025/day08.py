# Advent of Code 2025 - Day 8

from __future__ import annotations

import collections
import logging
from dataclasses import dataclass
from typing import LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def distance_to(self, other: Point3D) -> float:
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        ) ** 0.5


def get_input_data():
    return read_input(day=8, year=2025)


def parse_data(data: list[str]) -> list[Point3D]:
    parsed_data = []
    for line in data:
        if line.strip():
            x, y, z = map(int, line.split(","))
            parsed_data.append(Point3D(x, y, z))
    return parsed_data


def get_test_input_data() -> list[LiteralString]:
    data = """162,817,812
    57,618,57
    906,360,560
    592,479,940
    352,342,300
    466,668,158
    542,29,236
    431,825,988
    739,650,466
    52,470,668
    216,146,977
    819,987,18
    117,168,530
    805,96,715
    346,949,466
    970,615,88
    941,993,340
    862,61,35
    984,92,344
    425,690,689
"""
    return data.split("\n")


def compute_distances(points: list[Point3D]) -> list[tuple[float, tuple[int, int]]]:
    """Compute distances between all pairs of points.
    Store them in a 2d array
    Args:
        points (list[Point3D]): List of 3D points.
    """
    distances = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = points[i].distance_to(points[j])
            distances.append((dist, (i, j)))

    distances.sort(key=lambda x: x[0])
    return distances


def connecting_circuits(
    distances: list[tuple[float, tuple[int, int]]],
) -> dict[int, int]:
    """Connect circuits based on distances.
    Args:
        distances (list[tuple[float, tuple[int, int]]]): Sorted list of distances and point indices.
    """

    circuits = {}
    nb_circuits = 0

    for _, (i, j) in distances:
        if i not in circuits and j not in circuits:
            # New Circuit
            circuits[i] = nb_circuits
            circuits[j] = nb_circuits
            nb_circuits += 1
        elif i in circuits and j not in circuits:
            # i Already in a circuit
            circuits[j] = circuits[i]
        elif i not in circuits and j in circuits:
            # j Already in a circuit
            circuits[i] = circuits[j]
        else:
            # I and j already in circuits
            if circuits[i] != circuits[j]:
                # We need to merge the two circuits :
                circuit_to_change = circuits[j]
                for key in circuits:
                    if circuits[key] == circuit_to_change:
                        circuits[key] = circuits[i]

    circuits_by_length = collections.Counter(circuits.values())
    return circuits_by_length


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    distances = compute_distances(data)  # noqa
    circuits_by_length = connecting_circuits(distances[: 1000 + 1])  # noqa
    lengths = list(circuits_by_length.values())
    circuit_lengths = sorted(lengths, reverse=True)
    result = 1
    for length in circuit_lengths[:3]:
        result *= length
    return result


def part2() -> int:
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
