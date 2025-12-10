# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
import queue
import random
import sys
import threading
import time
from typing import LiteralString

import pygame

from aoc.utils import read_input

logger = logging.getLogger(__name__)


Color = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def get_input_data():
    return read_input(day=9, year=2025)


def parse_data(data: list[str]) -> list[complex]:
    """Return a list of complex numbers representing the points"""
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

    logger.debug(f"Max surface: {max_surface} between points {max_p1} and {max_p2}")

    return max_p1, max_p2, int(max_surface)


Vector = tuple[complex, complex]


def init_matrix(data: list[complex]) -> tuple[int, int, list[Vector]]:
    logger.debug(f"Number of data points: {len(data)}")

    vectors = []
    max_x = 0
    max_y = 0

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


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    _, _, max_surface = compute_surfaces(data)
    return max_surface


def get_rectangle(
    p1: complex,
    p2: complex,
) -> tuple[complex, complex, complex, complex]:
    """Return the rectangle defined by p1 and p2"""
    top_left = complex(min(p1.real, p2.real), min(p1.imag, p2.imag))
    top_right = complex(max(p1.real, p2.real), min(p1.imag, p2.imag))
    bottom_left = complex(min(p1.real, p2.real), max(p1.imag, p2.imag))
    bottom_right = complex(max(p1.real, p2.real), max(p1.imag, p2.imag))

    return top_left, top_right, bottom_left, bottom_right


def ccw(a: complex, b: complex, c: complex) -> bool:
    return (c.imag - a.imag) * (b.real - a.real) > (b.imag - a.imag) * (c.real - a.real)


DEFAULT_COLOR = (200, 200, 200)


def pygame_loop(
    cmd_queue: queue.Queue,
    event_queue: queue.Queue,
    width: int,
    height: int,
    title: str,
    fps: int = 60,
):
    logger.info("Starting Pygame visualization...")
    pygame.init()
    pygame.key.set_repeat(300, 40)
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()

    # ----- WINDOW = HALF THE SCREEN -----
    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h

    WIN_W = SCREEN_W // 2
    WIN_H = SCREEN_H // 2
    COEFF_W = WIN_W / (width + 2)
    COEFF_H = WIN_H / (height + 2)
    screen = pygame.display.set_mode((WIN_W, WIN_H))

    bg_color = (25, 25, 25)

    font_cache = {}

    def get_font(size: int) -> pygame.font.Font:
        if size not in font_cache:
            font_cache[size] = pygame.font.SysFont("Arial", size)
        return font_cache[size]

    running = True
    map: list[tuple[complex, complex]] = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.debug("QUIT event received in Pygame loop")
                running = False
                event_queue.put(event)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                logger.debug("ESCAPE key pressed, quitting Pygame loop")
                running = False
                event_queue.put(event)
            else:  # Forward other events to the event queue
                event_queue.put(event)

        try:
            while True:
                cmd, data = cmd_queue.get_nowait()
                if cmd == "QUIT":
                    running = False
                    pygame.quit()
                    sys.exit()
                elif cmd == "POINT":
                    point, color, size = data
                    pygame.draw.circle(
                        screen,
                        color,
                        (int(point.real * COEFF_W), int(point.imag * COEFF_H)),
                        size,
                    )
                elif cmd == "LINE":
                    start, end, color, width = data
                    pygame.draw.line(
                        screen,
                        color,
                        (int(start.real * COEFF_W), int(start.imag * COEFF_H)),
                        (int(end.real * COEFF_W), int(end.imag * COEFF_H)),
                        width,
                    )
                elif cmd == "RECTANGLE":
                    p1, p2, p3, p4, color, width = data
                    pygame.draw.polygon(
                        screen,
                        color,
                        [
                            (int(p1.real * COEFF_W), int(p1.imag * COEFF_H)),
                            (int(p2.real * COEFF_W), int(p2.imag * COEFF_H)),
                            (int(p4.real * COEFF_W), int(p4.imag * COEFF_H)),
                            (int(p3.real * COEFF_W), int(p3.imag * COEFF_H)),
                        ],
                        width,
                    )
                elif cmd == "MAP":
                    p1, p2 = data
                    map.append((p1, p2))
                elif cmd == "CLEAR":
                    screen.fill(bg_color)
                    for p1, p2 in map:
                        pygame.draw.line(
                            screen,
                            DEFAULT_COLOR,
                            (int(p1.real * COEFF_W), int(p1.imag * COEFF_H)),
                            (int(p2.real * COEFF_W), int(p2.imag * COEFF_H)),
                            1,
                        )
                elif cmd == "INIT":
                    cmd_queue.put(("CLEAR", None))

        except queue.Empty:
            pass

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    logger.info("Pygame visualization ended.")
    sys.exit()


def game_loop(cmd_queue: queue.Queue, event_queue: queue.Queue, data: list[complex]):
    running = True

    # Initialize game state here
    for i in range(len(data)):
        p1 = data[i]
        p2 = data[(i + 1) % len(data)]
        color = (200, 200, 200)
        cmd_queue.put(("MAP", (p1, p2)))
    cmd_queue.put(("INIT", None))

    # Getting through all points
    points = iter(data)

    while running:
        try:
            while True:
                event = event_queue.get_nowait()
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False

        except queue.Empty:
            pass

        cmd_queue.put(("CLEAR", None))

        try:
            point = next(points)
            color = get_random_color()
            cmd_queue.put(("POINT", (point, color, 5)))
        except StopIteration:
            pass

        time.sleep(0.016)  # Simulate ~60 FPS


def part2():
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa

    logger.info("Initializing base matrix...")
    max_x, max_y, base_matrix = init_matrix(data)
    logger.debug("Base matrix initialized")

    cmd_queue: queue.Queue = queue.Queue()
    event_queue: queue.Queue = queue.Queue()

    game_thread = threading.Thread(
        target=game_loop, args=(cmd_queue, event_queue, data)
    )
    game_thread.start()

    try:
        pygame_loop(
            cmd_queue,
            event_queue,
            max_x,
            max_y,
            title="Advent of Code 2025 - Day 9 Visualization",
        )
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, quitting...")
        event_queue.put(pygame.event.Event(pygame.QUIT))
        game_thread.join()
