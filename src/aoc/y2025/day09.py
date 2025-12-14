# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
import queue
import random
import sys
import threading
import time
from collections import defaultdict
from enum import Enum, auto
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
LOG_RATIO = 1000


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
) -> tuple[float, float, float, float, pygame.Surface]:
    logger.info("Starting Pygame visualization...")
    pygame.init()
    pygame.key.set_repeat(300, 40)
    pygame.display.set_caption(title)

    info = pygame.display.Info()
    SCREEN_W, SCREEN_H = info.current_w, info.current_h
    WIN_W = SCREEN_W // 2
    WIN_H = SCREEN_H // 2

    screen = pygame.display.set_mode((WIN_W, WIN_H))

    # --- 30% margin inside the window ---
    MARGIN_RATIO = 0.30

    INSET_W = WIN_W * MARGIN_RATIO / 2
    INSET_H = WIN_H * MARGIN_RATIO / 2

    DRAW_W = WIN_W * (1 - MARGIN_RATIO)
    DRAW_H = WIN_H * (1 - MARGIN_RATIO)

    # --- scaling factors for your grid ---
    COEFF_W = DRAW_W / width
    COEFF_H = DRAW_H / height

    return COEFF_W, COEFF_H, INSET_W, INSET_H, screen


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
    COEFF_W, COEFF_H, INSET_W, INSET_H, screen = pygame_init(title, width, height)

    # Send start event to the event queue
    event_queue.put(pygame.event.Event(pygame.USEREVENT + 3))

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
                        (
                            int(INSET_W + point.real * COEFF_W),
                            int(INSET_H + point.imag * COEFF_H),
                        ),
                        size,
                    )
                elif cmd == "LINE":
                    start, end, color, width = data
                    pygame.draw.line(
                        screen,
                        color,
                        (
                            int(INSET_W + start.real * COEFF_W),
                            int(INSET_H + start.imag * COEFF_H),
                        ),
                        (
                            int(INSET_W + end.real * COEFF_W),
                            int(INSET_H + end.imag * COEFF_H),
                        ),
                        width,
                    )
                elif cmd == "RECTANGLE":
                    p1, p2, p3, p4, color, width = data
                    pygame.draw.polygon(
                        screen,
                        color,
                        [
                            (
                                int(INSET_W + p1.real * COEFF_W),
                                int(INSET_H + p1.imag * COEFF_H),
                            ),
                            (
                                int(INSET_W + p2.real * COEFF_W),
                                int(INSET_H + p2.imag * COEFF_H),
                            ),
                            (
                                int(INSET_W + p3.real * COEFF_W),
                                int(INSET_H + p3.imag * COEFF_H),
                            ),
                            (
                                int(INSET_W + p4.real * COEFF_W),
                                int(INSET_H + p4.imag * COEFF_H),
                            ),
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
                            (
                                int(INSET_W + p1.real * COEFF_W),
                                int(INSET_H + p1.imag * COEFF_H),
                            ),
                            (
                                int(INSET_W + p2.real * COEFF_W),
                                int(INSET_H + p2.imag * COEFF_H),
                            ),
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
    WARNING_UP = auto()
    BUILD_PATH = auto()
    FIND_HORIZONTAL_SEGMENTS = auto()
    FIND_VERTICAL_SEGMENTS = auto()
    FIND_RECTANGLES = auto()
    END = auto()


def game_data(
    data: list[complex],
) -> tuple[dict[int, list[Vector]], dict[int, list[Vector]]]:
    """Build game data structures from input data
    Returns horizontal and vertical v_vectors
    """
    h_vectors: defaultdict[int, list[Vector]] = defaultdict(list)
    v_vectors: defaultdict[int, list[Vector]] = defaultdict(list)

    for i in range(len(data)):
        p1 = data[i]
        p2 = data[(i + 1) % len(data)]

        if p1.real == p2.real:
            # Vertical line
            v_vectors[int(p1.real)].append((p1, p2))
        elif p1.imag == p2.imag:
            # Horizontal line
            h_vectors[int(p1.imag)].append((p1, p2))
        else:
            logger.warning(f"Non-axis-aligned line between {p1} and {p2}, skipping")

    return dict(h_vectors), dict(v_vectors)


class PointPosition(Enum):
    INSIDE = auto()
    OUTSIDE = auto()
    ON_EDGE = auto()


def point_on_segment(p: complex, a: complex, b: complex, epsilon=1e-9) -> bool:
    """Check if point p is on segment a-b"""
    px, py = p.real, p.imag
    ax, ay = a.real, a.imag
    bx, by = b.real, b.imag

    # Horizontal segment
    if ay == by:
        if abs(py - ay) > epsilon:
            return False
        if min(ax, bx) - epsilon <= px <= max(ax, bx) + epsilon:
            return True
        return False

    # Vertical segment
    if ax == bx:
        if abs(px - ax) > epsilon:
            return False
        if min(ay, by) - epsilon <= py <= max(ay, by) + epsilon:
            return True
        return False

    return False


def raycast_right_axis(point: complex, path: list[complex]) -> int:
    """Count how many times a raycast to the right intersects the polygon edges"""
    logger.debug(f"Raycasting right from point {point}")
    px, py = point.real, point.imag
    count = 0
    n = len(path)

    for i in range(n):
        a = path[i]
        b = path[(i + 1) % n]
        ax, ay = a.real, a.imag
        bx, by = b.real, b.imag

        # Only vertical edges for horizontal raycast
        if ax != bx:
            continue

        # sort y so that ay <= by
        if ay > by:
            ay, by = by, ay

        # half open interval [ay, by]
        if ay <= py < by and ax >= px:
            count += 1

    logger.debug(f"Raycast right from point {point} intersected {count} times")
    return count


def raycast_up_axis(point: complex, path: list[complex]) -> int:
    """Count how many times a raycast upwards intersects the polygon edges"""
    px, py = point.real, point.imag
    count = 0
    n = len(path)

    for i in range(n):
        a = path[i]
        b = path[(i + 1) % n]
        ax, ay = a.real, a.imag
        bx, by = b.real, b.imag

        # Only horizontal edges for vertical raycast
        if ay != by:
            continue

        # sort x so that ax <= bx
        if ax > bx:
            ax, bx = bx, ax

        # half open interval [ax, bx]
        if ax <= px < bx and by >= py:
            count += 1

    return count


def point_position_on_horizontal_axis(
    point: complex, path: list[complex]
) -> PointPosition:
    """Determine if a point is inside, outside, or on the edge of a polygon using raycasting"""
    # Boundary first
    n = len(path)
    for i in range(n):
        if point_on_segment(point, path[i], path[(i + 1) % n]):
            return PointPosition.ON_EDGE

    # Raycast to the right
    intersection = raycast_right_axis(point, path)
    return PointPosition.INSIDE if intersection % 2 == 1 else PointPosition.OUTSIDE


def point_position_on_vertical_axis(
    point: complex, path: list[complex]
) -> PointPosition:
    """Determine if a point is inside, outside, or on the edge of a polygon using raycasting"""
    # Boundary first
    n = len(path)
    for i in range(n):
        if point_on_segment(point, path[i], path[(i + 1) % n]):
            return PointPosition.ON_EDGE

    # Raycast upwards
    intersection = raycast_up_axis(point, path)
    return PointPosition.INSIDE if intersection % 2 == 1 else PointPosition.OUTSIDE


def longest_horizontal_segment(
    point: complex,
    path: list[complex],
    step: float = 1,  # Avoid to consecutive vertical vectors
) -> tuple[complex, complex] | None:
    """Find the longest horizontal segment (left, right) from the point along y axis that stays inside the polygon or on the get_boundaries"""
    x, y = point.real, point.imag

    def in_or_on(xt: float) -> bool:
        pos = point_position_on_horizontal_axis(complex(xt, y), path)
        return pos in (PointPosition.INSIDE, PointPosition.ON_EDGE)

    if not in_or_on(x):
        return None

    # Expand left
    logger.debug(f"Finding left boundary from x={x}, y={y}")
    left_x = x
    while in_or_on(left_x - step):
        left_x -= step

    # Expand right
    logger.debug(f"Finding right boundary from x={x}, y={y}")
    right_x = x
    while in_or_on(right_x + step):
        right_x += step

    return complex(left_x, y), complex(right_x, y)


def longest_vertical_segment(
    point: complex,
    path: list[complex],
    step: float = 0.5,  # Avoid to consecutive horizontal vectors
) -> tuple[complex, complex] | None:
    """Find the longest vertical segment (up, down) from the point along x axis that stays inside the polygon or on the get_boundaries"""
    x, y = point.real, point.imag

    def in_or_on(yt: float) -> bool:
        pos = point_position_on_vertical_axis(complex(x, yt), path)
        return pos in (PointPosition.INSIDE, PointPosition.ON_EDGE)

    if not in_or_on(y):
        return None

    # Expand down
    down_y = y
    while in_or_on(down_y - step):
        down_y -= step

    # Expand up
    up_y = y
    while in_or_on(up_y + step):
        up_y += step

    return complex(x, down_y), complex(x, up_y)


def game_loop(
    cmd_queue: queue.Queue,
    event_queue: queue.Queue,
    data: list[complex],
) -> int:
    logger.info("Starting game loop...")
    running = True
    step_mode = False
    step = False
    phase = Phase.BUILD_PATH

    max_area = 0
    max_rectangle = (0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j)
    horizontal_segments: list[tuple[complex, tuple[complex, complex]]] = []

    points = iter(data)

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
                elif event.type == pygame.USEREVENT + 3:
                    logger.debug("Starting game")
                    phase = Phase.BUILD_PATH

        except queue.Empty:
            pass

        if step_mode and not step:
            time.sleep(0.01)
            continue

        if phase == Phase.WARNING_UP:
            logger.info("Processing WARNING_UP phase")
            time.sleep(1)

        elif phase == Phase.BUILD_PATH:
            cmd_queue.put(("CLEAR", None))
            cmd_queue.put(("INIT", None))

            for i in range(len(data)):
                p1 = data[i]
                p2 = data[(i + 1) % len(data)]

                cmd_queue.put(
                    (
                        "MAP",
                        (p1, p2),
                    )
                )

            phase = Phase.FIND_HORIZONTAL_SEGMENTS
            logger.info("Completed BUILD_PATH phase")

        elif phase == Phase.FIND_HORIZONTAL_SEGMENTS:
            logger.info("Processing FIND_HORIZONTAL_SEGMENTS phase")

            try:
                point = next(points)
                logger.debug(f"Processing point {point}")
            except StopIteration:
                logger.info("No more points to process, ending game loop")
                phase = Phase.END
                continue

            logger.debug(f"Finding longest horizontal segment for point {point}")
            horizontal_segment = longest_horizontal_segment(point, data)
            if horizontal_segment is not None:
                cmd_queue.put(
                    (
                        "LINE",
                        (
                            horizontal_segment[0],
                            horizontal_segment[1],
                            Color["green"],
                            2,
                        ),
                    )
                )
                horizontal_segments.append((point, horizontal_segment))
        elif phase == Phase.END:
            running = False
            logger.info("Reached END phase, exiting game loop")
            continue

        time.sleep(0.01)  # Simulate some processing delay
        step = False

    logger.info(f"Max rectangle area found: {max_area}")
    logger.info(f"Max rectangle corners: {max_rectangle}")
    return int(max_area)


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
