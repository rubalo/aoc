# Advent of Code 2025 - Day 10

from __future__ import annotations

import logging
import re
from collections import deque
from typing import Deque, LiteralString

from aoc.utils import read_input

logger = logging.getLogger(__name__)


# Parser for a machine like:
# [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
re_pattern = re.compile(
    r"^(?P<diagram>\[([.#]+)\])\s"
    r"(?P<buttons>(?:\(\s*[^)]*\s*\)\s*)+)\s"
    r"(?P<joltages>\{([0-9]+(,[0-9]+)*)\})$"
)


class Machine:
    diagram: list[str]
    buttons: list[tuple]
    joltages: set[int]

    def __init__(self, line: str):
        self.parse_input(line)

    def parse_input(self, line: str):
        logger.debug(f"Parsing line: {line}")

        match = re_pattern.match(line.strip())

        if not match:
            raise ValueError(f"Line does not match pattern: {line}")
        diagram_str = match.group("diagram")
        buttons_str = match.group("buttons")
        joltages_str = match.group("joltages")
        self.diagram = list(diagram_str[1:-1])
        self.buttons = [
            tuple(int(num) for num in btn.strip("()").split(","))
            for btn in buttons_str.strip().split()
        ]
        self.joltages = set(
            int(jolt.strip()) for jolt in joltages_str.strip("{}").split(",")
        )

    def __str__(self):
        return f"Machine(diagram={self.diagram}, buttons={self.buttons}, joltages={self.joltages})"

    def index_to_flip(self, state: list[str]) -> list[int]:
        """Determine which index to flip to make the machine ready.
        [....] -> [.##.] will return [1,2]
        """
        indices = []
        for i, (d, s) in enumerate(zip(self.diagram, state)):
            if d != s:
                indices.append(i)
        return indices

    def list_buttons(self, indexes: list[int]) -> list[int]:
        """Check if the given indexes can be flipped with any button.
        Returns a list of the button that needs to be pressed to flip those indexes.
        """
        buttons = []
        for i, button in enumerate(self.buttons):
            if any([index in button for index in indexes]):
                buttons.append(i)
        return buttons

    def push_button(self, state: list[str], button_number: int) -> list[str]:
        """Push the given button to flip the indexes."""
        button = self.buttons[button_number]
        new_state = state.copy()
        for index in button:
            if state[index] == ".":
                new_state[index] = "#"
            else:
                new_state[index] = "."

        return new_state

    def activated(self, state: list[str]) -> bool:
        return self.diagram == state

    def initial_state(self) -> list[str]:
        return ["." for _ in self.diagram]


def get_input_data():
    return read_input(day=10, year=2025)


def parse_data(data: list[str]) -> list[Machine]:
    machines = []
    for line in data:
        if not line.strip():
            continue
        machines.append(Machine(line))
    return machines


def get_test_input_data() -> list[LiteralString]:
    data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
    return data.split("\n")


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    result = 0
    queue: Deque[tuple[list[str], list[int]]] = deque()

    for m in data:
        logger.info(f"Processing machine: {m}")
        queue.append((m.initial_state(), []))

        while queue:
            state, buttons_pressed = queue.popleft()
            logger.debug(f"Current state: {state}, buttons pressed: {buttons_pressed}")
            wrong_indexes = m.index_to_flip(state)
            possible_buttons = m.list_buttons(wrong_indexes)
            for button in possible_buttons:
                new_state = m.push_button(state, button)
                new_buttons_pressed = buttons_pressed.copy() + [button]

                if m.activated(new_state):
                    result += len(new_buttons_pressed)
                    logger.info(
                        f"Machine activated with buttons: {new_buttons_pressed}, nb buttons: {len(new_buttons_pressed)}"
                    )
                    queue.clear()
                    break
                else:
                    queue.append((new_state, new_buttons_pressed))

    return result


def part2() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    return 0
