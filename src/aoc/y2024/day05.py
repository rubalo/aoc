# Advent of Code 2024 - Day 5

from __future__ import annotations

from aoc.utils import read_input

PREDS = {}


def get_input_data() -> list[str]:
    return read_input(day=5, year=2024)


def get_test_input_data() -> list[str]:
    test_input = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    return [str(x) + "\n" for x in test_input.split("\n")]


def parse_data(data: list[str]) -> tuple[list[tuple[int, int]], list[list[int]]]:
    i = data.index("\n")
    part1 = data[:i]
    part2 = data[i + 1 :]

    constraints = []
    for line in part1:
        a, b = line.rstrip().split("|")
        constraints.append((int(a), int(b)))

    constraints = sorted(constraints, key=lambda x: x[0])

    print_list = [[int(x) for x in line.rstrip().split(",")] for line in part2]

    return constraints, print_list


def parse_constraints(constraints: list[tuple[int, int]]):
    for constraint in constraints:
        a, b = constraint
        if b not in PREDS:
            PREDS[b] = set()
        PREDS[b].add(a)


def check_successors(page: int, successors: list[int]) -> bool:
    return all(
        page not in PREDS or successor not in PREDS[page] for successor in successors
    )


def part1() -> int:
    data = get_input_data()

    constraints, print_lists = parse_data(data)

    parse_constraints(constraints)

    res = 0

    good_list, _ = sort_lists(print_lists)

    for print_list in good_list:
        mid = len(print_list) // 2
        res += print_list[mid]

    return res


def sort_lists(print_lists: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    good_lists = []
    bad_lists = []

    for print_list in print_lists:
        if check_list(print_list):
            good_lists.append(print_list)
        else:
            bad_lists.append(print_list)

    return good_lists, bad_lists


def check_list(print_list: list[int]) -> bool:
    for i, page in enumerate(print_list[:-1]):
        # Check page against its successors
        page = print_list[i]  # noqa
        successors = print_list[i + 1 :]
        if not check_successors(page, successors):
            return False
    return True


def fix_list(print_list: list[int]) -> list[int]:
    wl = print_list.copy()

    while not check_list(wl):
        for i in range(len(wl) - 1):
            page = wl[i]
            for j in range(i + 1, len(wl)):
                successor = wl[j]
                if page in PREDS and successor in PREDS[page]:
                    wl[i], wl[j] = wl[j], wl[i]
                    break
            else:
                continue
            break
    return wl


def part2() -> int:
    data = get_input_data()

    constraints, print_lists = parse_data(data)

    parse_constraints(constraints)

    res = 0

    _, bad_list = sort_lists(print_lists)

    fixed_list = []

    for print_list in bad_list:
        while not check_list(print_list):
            print_list = fix_list(print_list)  # noqa
        fixed_list.append(fix_list(print_list))

    for print_list in fixed_list:
        mid = len(print_list) // 2
        res += print_list[mid]

    return res
