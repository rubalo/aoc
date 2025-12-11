# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
import queue
import random
import sys
import threading
import time
from typing import Iterator, LiteralString

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
DEFAULT_COLOR = (200, 200, 200)
BG_COLOR = (25, 25, 25)


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


def part1() -> int:
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    _, _, max_surface = compute_surfaces(data)
    return max_surface


def pygame_init(
    title: str, width: int, height: int
) -> tuple[float, float, pygame.Surface]:
    logger.info("Starting Pygame visualization...")
    pygame.init()
    pygame.key.set_repeat(300, 40)
    pygame.display.set_caption(title)

    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h
    WIN_W = SCREEN_W // 2
    WIN_H = SCREEN_H // 2
    COEFF_W = WIN_W / (width + 2)
    COEFF_H = WIN_H / (height + 2)

    screen = pygame.display.set_mode((WIN_W, WIN_H))

    return COEFF_W, COEFF_H, screen


def pygame_loop(
    cmd_queue: queue.Queue,
    event_queue: queue.Queue,
    width: int = 800,
    height: int = 600,
    title: str = "Pygame Visualization",
    fps: int = 60,
):
    clock = pygame.time.Clock()
    logger.info("Initializing Pygame...")
    COEFF_W, COEFF_H, screen = pygame_init(title, width, height)

    running = True
    map: list[tuple[complex, complex]] = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.debug("QUIT event received in Pygame loop")
                running = False
                event_queue.put(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    logger.debug("ESCAPE key pressed, quitting Pygame loop")
                    running = False
                    event_queue.put(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_SPACE:
                    logger.debug("SPACE key pressed, toggling step mode")
                    event_queue.put(pygame.event.Event(pygame.USEREVENT + 1))
                else:
                    logger.debug(f"Key {event.key} pressed, forwarding event")
                    event_queue.put(pygame.event.Event(pygame.USEREVENT + 2))
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
                            (int(p3.real * COEFF_W), int(p3.imag * COEFF_H)),
                            (int(p4.real * COEFF_W), int(p4.imag * COEFF_H)),
                        ],
                        width,
                    )
                elif cmd == "MAP":
                    p1, p2 = data
                    map.append((p1, p2))
                elif cmd == "CLEAR":
                    screen.fill(BG_COLOR)
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
                    screen.fill(BG_COLOR)

        except queue.Empty:
            pass

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    logger.info("Pygame visualization ended.")
    sys.exit()


def get_boundaries(data: list[complex]) -> tuple[int, int]:
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    for point in data:
        if point.real < min_x:
            min_x = int(point.real)
        if point.real > max_x:
            max_x = int(point.real)
        if point.imag < min_y:
            min_y = int(point.imag)
        if point.imag > max_y:
            max_y = int(point.imag)
    return max_x, max_y


def build_Path(data: list[complex]) -> Iterator[Vector]:
    """Build a path connecting all points in data"""
    for i in range(len(data)):
        yield (data[i], data[(i + 1) % len(data)])


class Phase:
    BUILD_PATH = 0


def game_loop(
    cmd_queue: queue.Queue,
    event_queue: queue.Queue,
    data: list[complex],
) -> None:
    logger.info("Starting game loop...")
    running = True
    step_mode = False
    step = False

    # Initial phase
    phase = Phase.BUILD_PATH
    path_vectors = build_Path(data)

    while running:
        try:
            while True:
                event = event_queue.get_nowait()
                if event.type == pygame.QUIT:
                    running = False
                    logger.debug("QUIT event received in game loop")
                    sys.exit()
                elif event.type == pygame.USEREVENT + 1:
                    logger.debug("Toggle step mode event received")
                    step_mode = not step_mode
                elif step_mode and event.type == pygame.USEREVENT + 2:
                    logger.debug("Step event received")
                    step = True

        except queue.Empty:
            pass

        if step_mode and not step:
            time.sleep(0.1)
            continue

        # PHASE: BUILD PATH
        if phase == Phase.BUILD_PATH:
            try:
                vector = next(path_vectors)
                cmd_queue.put(("LINE", (vector[0], vector[1], get_random_color(), 2)))
            except StopIteration:
                phase = None  # End of phases

        time.sleep(0.016)  # Simulate some processing delay
        step = False

    return None


def part2():
    data = get_input_data()  # noqa
    data = parse_data(data)  # noqa
    result = 0

    cmd_queue: queue.Queue = queue.Queue()
    event_queue: queue.Queue = queue.Queue()

    # Is visualization enabled?
    if "-v" in sys.argv:
        logger.info("Visualization enabled")

        width, height = get_boundaries(data)

        game_thread = threading.Thread(
            target=game_loop, args=(cmd_queue, event_queue, data)
        )
        game_thread.start()

        try:
            pygame_loop(
                cmd_queue,
                event_queue,
                width,
                height,
                title="Advent of Code 2025 - Day 9 Visualization",
            )
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt received, quitting...")
            # Send an event to the game loop to quit
            cmd_queue.put(("QUIT", None))
            # Send an end event to the event queue to quit
            event_queue.put(pygame.event.Event(pygame.QUIT))
            game_thread.join()

    else:
        logger.info("Visualization disabled")
        result = game_loop(cmd_queue, event_queue, data)
    return result
