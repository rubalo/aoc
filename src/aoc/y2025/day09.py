# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
import sys
from typing import Iterable, LiteralString

import pygame

from aoc.utils import read_input

logger = logging.getLogger(__name__)


def get_input_data():
    return read_input(day=9, year=2025)


def parse_data(data: list[str]) -> list[complex]:
    input = []
    for line in data:
        if line.strip() == "":
            continue

        x, y = line.split(",")
        input.append(complex(int(x), int(y)))

    return input


def get_test_input_data() -> list[LiteralString]:
    data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""
    return data.split("\n")


def compute_surfaces(data: list[complex]) -> tuple[complex, complex, int]:
    max_surface = 0
    max_p1 = 0 + 0j
    max_p2 = 0 + 0j
    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            p1 = data[i]
            p2 = data[j]

            width = abs(p2.real - p1.real) + 1
            height = abs(p2.imag - p1.imag) + 1
            area = width * height
            logger.debug(f"Area between {p1} and {p2}: {area}")
            if area > max_surface:
                max_surface = area
                max_p1 = p1
                max_p2 = p2

    logger.info(f"Max surface: {max_surface} between points {max_p1} and {max_p2}")

    return max_p1, max_p2, int(max_surface)


Vector = tuple[complex, complex]


def init_matrix(data: list[complex]) -> tuple[int, int, list[Vector]]:
    logger.debug(f"Number of data points: {len(data)}")

    vectors = []
    max_x = 0
    max_y = 0

    # Close the loop
    data.append(data[0])

    for i in range(len(data) - 1):
        p1 = data[i]
        p2 = data[i + 1]
        t_max_x = int(max(p1.real, p2.real))
        t_max_y = int(max(p1.imag, p2.imag))
        logger.debug(f"Line from {p1} to {p2}")
        vectors.append((p1, p2))
        if t_max_x > max_x:
            max_x = t_max_x
        if t_max_y > max_y:
            max_y = t_max_y

    return max_x, max_y, vectors


def find_best_font_size(win_w: int, win_h: int, grid_w: int, grid_h: int) -> int:
    size = 1
    best = 1

    font = pygame.font.SysFont("monospace", size)
    glyph = font.render("A", True, (255, 255, 255))
    char_w, char_h = glyph.get_size()

    total_w = char_w * grid_w
    total_h = char_h * grid_h

    while total_w < win_w and total_h < win_h:
        best = size
        size += 1
        font = pygame.font.SysFont("monospace", size)
        glyph = font.render("A", True, (255, 255, 255))
        char_w, char_h = glyph.get_size()
        total_w = char_w * grid_w
        total_h = char_h * grid_h
    return best


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    _, _, max_surface = compute_surfaces(data)
    return max_surface


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                waiting = False


def get_rectangle(
    data: list[Vector],
) -> Iterable[tuple[complex, complex, complex, complex]]:

    # Close the loop
    data.append((data[0][0], data[0][1]))

    interior = ccw(data[0][0], data[0][1], data[1][1])

    for i in range(len(data) - 1):
        p1, p2 = data[i]
        p3, p4 = data[i + 1]
        assert p2 == p3, "Vectors are not connected"
        if ccw(p1, p2, p4) != interior:
            continue

        pr = p1 + (p4 - p3)

        yield (p1, p2, p4, pr)


def ccw(a: complex, b: complex, c: complex) -> bool:
    return (c.imag - a.imag) * (b.real - a.real) > (b.imag - a.imag) * (c.real - a.real)


def part2():
    data = get_input_data()  # noqa
    data = get_test_input_data()  # noqa
    data = parse_data(data)  # noqa

    logger.info("Starting Pygame visualization...")
    pygame.init()

    logger.info("Initializing base matrix...")
    max_x, max_y, base_matrix = init_matrix(data)
    logger.debug("Base matrix initialized")

    # ----- WINDOW = HALF THE SCREEN -----
    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h

    WIN_W = SCREEN_W // 2
    WIN_H = SCREEN_H // 2
    COEFF_W = WIN_W / (max_x + 2)
    COEFF_H = WIN_H / (max_y + 2)

    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Advent of Code 2025 - Day 9 Visualization")

    clock = pygame.time.Clock()
    running = True
    first_frame = True
    matrix = base_matrix
    rectangles = get_rectangle(base_matrix)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for vector in matrix:
            p1, p2 = vector
            pygame.draw.line(
                screen,
                (255, 255, 255),
                (int(p1.real * COEFF_W), int(p1.imag * COEFF_H)),
                (int(p2.real * COEFF_W), int(p2.imag * COEFF_H)),
                2,
            )
        if not first_frame:
            try:
                p1, p2, p3, p4 = next(rectangles)
            except StopIteration:
                running = False
                continue
            pygame.draw.polygon(
                screen,
                (0, 255, 0),
                [
                    (int(p1.real * COEFF_W), int(p1.imag * COEFF_H)),
                    (int(p2.real * COEFF_W), int(p2.imag * COEFF_H)),
                    (int(p3.real * COEFF_W), int(p3.imag * COEFF_H)),
                    (int(p4.real * COEFF_W), int(p4.imag * COEFF_H)),
                ],
                2,
            )
        first_frame = False

        pygame.display.flip()
        wait_for_key()
        clock.tick(60)

    pygame.quit()
    return 0
