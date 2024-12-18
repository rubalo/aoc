# Advent of Code 2024 - Day 12

from __future__ import annotations

from typing import LiteralString

import numpy as np

from aoc.utils import read_input

UP = -1 + 0j
DOWN = 1 + 0j
LEFT = 0 - 1j
RIGHT = 0 + 1j

MAX_NEIGHBORS = 4


def get_input_data():
    return read_input(day=12, year=2024)


def parse_data(data: list[str]):
    return np.array([np.array(list(line.rstrip())) for line in data])


def get_test_input_data() -> list[LiteralString]:
    data = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO"""
    data = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    data = """AAAA
BBCD
BBCC
EEEC"""
    return data.split("\n")


class Zone:
    plant: str
    plots: set
    top: int
    bottom: int
    left: int
    right: int
    neighbours: dict[complex, list[complex]]

    def __init__(self, plant, plots: set):
        self.plots = plots
        self.plant = plant
        self.top, self.bottom, self.left, self.right = self.borders()
        self.neighbours = {plot: self._get_neighbours(plot)[0] for plot in self.plots}
        self.boundaries = self._get_boundaries()
        self.ordered_boundaries()

    def borders(self) -> tuple[int, int, int, int]:
        xs = [int(x.real) for x in self.plots]
        ys = [int(y.imag) for y in self.plots]
        top = min(xs)
        bottom = max(xs)
        left = min(ys)
        right = max(ys)
        return top, bottom, left, right

    @property
    def area(self):
        return len(self.plots)

    @property
    def perimeter(self):
        p_len = 0
        for plot in self.plots:
            neighbours = self.neighbours[plot]
            p_len += MAX_NEIGHBORS - len(neighbours)

        return p_len

    def _get_neighbours(self, plot: complex) -> tuple[list[complex], list[complex]]:
        neighbours = []
        not_neighbours = [plot + UP, plot + DOWN, plot + LEFT, plot + RIGHT]
        for t_plot in self.plots:
            if plot == t_plot:
                continue

            if abs(plot - t_plot) == 1:
                neighbours.append(t_plot)
                not_neighbours.remove(t_plot)

        return neighbours, not_neighbours

    def _get_boundaries(self) -> list[tuple[complex, complex]]:
        boundaries = []
        for plot in self.plots:
            _, not_neighbours = self._get_neighbours(plot)
            for n_plot in not_neighbours:
                boundaries.append((plot, n_plot))

        return boundaries

    def ordered_boundaries(self) -> None:
        boundaries = sorted(self.boundaries.copy(), key=lambda x: (x[0].real, x[0].imag))
        start_point = boundaries.pop()
        ordered_boundaries = [start_point]
        print("*" * 10)
        print(self)
        print(boundaries)
        print(ordered_boundaries)
        print("*" * 10)


        self.boundaries = ordered_boundaries

    def get_nb_faces(self) -> int:
        return 0


    def aligned_with_neighbours(self, plot: complex) -> bool:
        neighbours = self.neighbours[plot]
        if all([plot.real == n.real for n in neighbours]):
            return True
        if all([plot.imag == n.imag for n in neighbours]):
            return True
        return False


    def __str__(self) -> str:
        return f"Plant: {self.plant}, area: {self.area}, perimeter: {self.perimeter}, tl: {self.top, self.left}, br: {self.bottom, self.right}, plots: {self.plots}"


def print_map(data: np.array) -> None:
    for i, row in enumerate(data):
        for j in range(len(row)):
            print(data[i, j], end="")  # noqa
        print("")  # noqa


def walk_zone(plant: str, plot: complex, data: np.array, visited: set) -> list[complex]:
    if plot in visited:
        return []

    x, y = int(plot.real), int(plot.imag)

    if x < 0 or y < 0 or x >= len(data) or y >= len(data[0]):
        return []

    if data[x, y] != plant:
        return []

    plots = [plot]
    visited.add(plot)
    plots.extend(walk_zone(plant, plot + UP, data, visited))
    plots.extend(walk_zone(plant, plot + DOWN, data, visited))
    plots.extend(walk_zone(plant, plot + LEFT, data, visited))
    plots.extend(walk_zone(plant, plot + RIGHT, data, visited))

    return plots


def build_zones(data) -> list[Zone]:
    visited = set()
    zones = []

    for i, row in enumerate(data):
        for j in range(len(row)):
            plot = complex(i, j)
            plant = str(data[i, j])
            if plot in visited:
                continue

            plots = walk_zone(plant, plot, data, set())
            zones.append(Zone(plant, set(plots)))
            visited.update(plots)

    return zones


def print_zones(zones: list[Zone]):
    for zone in zones:
        print(zone)  # noqa


def part1() -> int:
    data = get_input_data()
    # data = get_test_input_data()
    mat = parse_data(data)
    # print_map(mat)
    zones = build_zones(mat)
    # print_zones(zones)
    res = 0
    for zone in zones:
        res += zone.area * zone.perimeter
    return res


def part2() -> int:
    data = get_input_data()
    data = get_test_input_data()
    mat = parse_data(data)
    print_map(mat)
    zones = build_zones(mat)
    res = 0
    for zone in zones:
        print(zone)
        print(zone.boundaries)
    return res
