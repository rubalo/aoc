import logging
from typing import LiteralString, Protocol

from aoc.utils import read_input

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class IDValidator(Protocol):
    def __call__(self, id_str: str) -> bool: ...


def id_repeated_twice(id_str: str) -> bool:
    if len(id_str) % 2 != 0:
        return False
    half_length = len(id_str) // 2
    if id_str[:half_length] != id_str[half_length:]:
        return False
    return True


def id_repeated_at_least_twice(id_str: str) -> bool:
    length = len(id_str)
    for i in range(length, 1, -1):
        if length % i != 0:
            continue
        part_length = length // i
        part = id_str[:part_length]
        if part * i == id_str:
            logger.debug(f"ID {id_str} is repeated at least twice as {part} * {i}")
            return True
    return False


def get_input_data():
    return read_input(day=2, year=2025)


def parse_data(data: list[str]):
    parsed_ranges = []
    for data_line in data:
        for range_pair in data_line.split(","):
            range_pair = range_pair.strip()
            if not range_pair:
                continue
            start_str, end_str = range_pair.split("-")
            start_int = int(start_str)
            end_int = int(end_str)
            parsed_ranges.append((start_int, end_int))
    return parsed_ranges


def get_test_input_data() -> list[LiteralString]:
    data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862"""
    return data.split("\n")


def detect_invalid_ids(
    ranges: list[tuple[int, int]], funcs: list[IDValidator]
) -> list[int]:
    invalid_ids = []
    for start, end in ranges:
        logger.debug(f"Checking range: {start}-{end}")
        for id_num in range(start, end + 1):
            id_str = str(id_num)
            for func in funcs:
                if func(id_str):
                    logger.debug(f"Invalid ID found: {id_str}")
                    invalid_ids.append(id_num)

    return invalid_ids


def part1() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)
    funcs = [id_repeated_twice]
    invalid_ids = detect_invalid_ids(parsed_data, funcs)
    return sum(invalid_ids)


def part2() -> int:
    data = get_input_data()  # noqa
    parsed_data = parse_data(data)
    funcs = [id_repeated_at_least_twice]
    invalid_ids = detect_invalid_ids(parsed_data, funcs)
    return sum(invalid_ids)
