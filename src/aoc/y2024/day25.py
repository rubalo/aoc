# Advent of Code 2024 - Day 25

from __future__ import annotations

from enum import Enum
from typing import LiteralString

from aoc.utils import read_input

SCHEMA_HEIGHT = 8
MAX_HEIGHT = 5


class SchemaType(Enum):
    LOCK = "lock"
    KEY = "key"


class Schema:
    schema_type: SchemaType
    heights = list[int]
    raw = list[str]

    def __init__(
        self, schema_type: SchemaType, heights: list[int], raw: list[str]
    ) -> None:
        self.schema_type = schema_type
        self.heights = heights
        self.raw = raw
        if self.raw[-1] == "":
            self.raw = self.raw[:-1]

    def __repr__(self) -> str:
        raw = "\n".join([f"        {line}" for line in self.raw])
        output = f""" *******
Schema(type={self.schema_type}, heights={self.heights})
{raw}
        """
        return output


def get_input_data():
    return read_input(day=25, year=2024)


def parse_data(data: list[str]) -> list[Schema]:

    schemas = []

    for i in range(0, len(data), SCHEMA_HEIGHT):
        raw_schema = [x.strip() for x in data[i : i + SCHEMA_HEIGHT]]

        key_lock_schema = raw_schema[1 : 1 + MAX_HEIGHT]
        h0 = [x[0] for x in key_lock_schema].count("#")
        h1 = [x[1] for x in key_lock_schema].count("#")
        h2 = [x[2] for x in key_lock_schema].count("#")
        h3 = [x[3] for x in key_lock_schema].count("#")
        h4 = [x[4] for x in key_lock_schema].count("#")

        if raw_schema[0].startswith("#"):
            schema_type = SchemaType.LOCK
        else:
            schema_type = SchemaType.KEY
        heights = [h0, h1, h2, h3, h4]

        schemas.append(Schema(schema_type, heights, raw_schema))

    return schemas


def get_test_input_data() -> list[LiteralString]:
    data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()  # noqa
    p_data = parse_data(data)

    locks = [schema for schema in p_data if schema.schema_type == SchemaType.LOCK]
    keys = [schema for schema in p_data if schema.schema_type == SchemaType.KEY]

    overlaps = 0

    for lock in locks:
        for key in keys:
            heights = [h1 + h2 for h1, h2 in zip(lock.heights, key.heights)]
            if any(h > MAX_HEIGHT for h in heights):
                print(
                    f"Overlap found!\nLock:\n{lock.heights}\nKey:\n{key.heights}\nHeights: {heights}\n"
                )
                continue
            print(
                f"Match found!\nLock:\n{lock.heights}\nKey:\n{key.heights}\nHeights: {heights}\n"
            )
            overlaps += 1

    return overlaps


def part2() -> int:
    data = get_input_data()  # noqa
    return 0
