# Advent of Code 2025 - Day 9

from __future__ import annotations

import logging
import queue
import random
import sys
import threading
import time
from collections import defaultdict
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
    BUILD_PATH = 0
    FIND_DIAGONALS = 1
    FIND_RECTANGLES = 2


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


def point_in_segment(p: complex, a: complex, b: complex) -> bool:
    """Check if point p is on the segment ab"""
    cross_product = (p.imag - a.imag) * (b.real - a.real) - (p.real - a.real) * (
        b.imag - a.imag
    )
    if abs(cross_product) > 1e-6:
        return False  # Not collinear

    dot_product = (p.real - a.real) * (b.real - a.real) + (p.imag - a.imag) * (
        b.imag - a.imag
    )
    if dot_product < 0:
        return False  # p is before a

    squared_length_ab = (b.real - a.real) ** 2 + (b.imag - a.imag) ** 2
    if dot_product > squared_length_ab:
        return False  # p is after b

    return True


def point_in_path(p: complex, path: list[complex]) -> bool:
    """Determine if the point in INSIDE, OUTSIDE or ON the path defined by the vectors"""
    n = len(path)
    if n < 3:
        return False  # A path with less than 3 segments cannot enclose an area

    # Test if point is on any segment
    for i in range(n):
        a = path[i]
        b = path[(i + 1) % n]
        if point_in_segment(p, a, b):
            return True

    # Ray-casting algorithm to determine if point is inside the polygon
    inside = False
    x, y = p.real, p.imag

    for i in range(n):
        a = path[i]
        b = path[(i + 1) % n]

        ax, ay = a.real, a.imag
        bx, by = b.real, b.imag

        if (ay > y) != (by > y):
            slope = (bx - ax) * (y - ay) / (by - ay) + ax
            if x < slope:
                inside = not inside

    return inside


def get_rectangle_corners(
    p1: complex, p2: complex
) -> tuple[complex, complex, complex, complex]:
    """Given two opposite corners of a rectangle, return all four corners"""
    return (
        complex(p1.real, p1.imag),
        complex(p2.real, p1.imag),
        complex(p2.real, p2.imag),
        complex(p1.real, p2.imag),
    )


def game_loop(
    cmd_queue: queue.Queue,
    event_queue: queue.Queue,
    data: list[complex],
) -> int:
    logger.info("Starting game loop...")
    running = True
    step_mode = False
    step = False

    # Build phase
    phase = Phase.BUILD_PATH
    path_vectors = build_Path(data)

    # Find diagonals phase
    phase2_iter = find_valid_diagonals(data)
    valid_pairs: list[tuple[complex, complex]] = []
    max_area = 0
    max_rectangle = (0 + 0j, 0 + 0j, 0 + 0j, 0 + 0j)

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
            time.sleep(0.01)
            continue

        # PHASE: BUILD PATH
        if phase == Phase.BUILD_PATH:
            logger.info("Building path...")
            for vector in path_vectors:
                cmd_queue.put(("MAP", vector))
                cmd_queue.put(("LINE", (vector[0], vector[1], DEFAULT_COLOR, 1)))
            phase = Phase.FIND_DIAGONALS
            logger.info("Finding valid diagonals...")

        elif phase == Phase.FIND_DIAGONALS:
            cmd_queue.put(("CLEAR", None))
            cpt = 0
            n = len(data) * (len(data) - 1) // 2
            for point1, point2, valid in phase2_iter:
                logger.debug(f"Processing diagonal ({point1}, {point2}), valid={valid}")
                cpt += 1
                if cpt % LOG_RATIO == 0:
                    logger.info(f"Processed {cpt}/{n} diagonals...")

                if valid:
                    cmd_queue.put(("CLEAR", None))
                    cmd_queue.put(
                        (
                            "LINE",
                            (point1, point2, Color["green"], 2),
                        )
                    )
                    valid_pairs.append((point1, point2))
                else:
                    cmd_queue.put(
                        (
                            "LINE",
                            (point1, point2, Color["red"], 2),
                        )
                    )
            phase = Phase.FIND_RECTANGLES
            logger.info("No more diagonals to process.")
        elif phase == Phase.FIND_RECTANGLES:
            logger.info("Finding maximum rectangles from valid diagonals...")
            cpt = 0
            n = len(valid_pairs)
            for point1, point2 in valid_pairs:
                logger.debug(
                    f"Checking rectangle {cpt + 1}/{n} with corners {point1}, {point2}"
                )
                cpt += 1
                if cpt % LOG_RATIO == 0:
                    logger.info(f"Processed {cpt}/{n} rectangles...")

                cmd_queue.put(("CLEAR", None))
                mp1, mp2, mp3, mp4 = max_rectangle
                cmd_queue.put(("RECTANGLE", (mp1, mp2, mp3, mp4, Color["yellow"], 2)))

                p1, p2, p3, p4 = get_rectangle_corners(point1, point2)
                logger.debug(f"Checking rectangle corners: {p1}, {p2}, {p3}, {p4}")

                cmd_queue.put(
                    (
                        "POINT",
                        (p1, Color["blue"], 5),
                    )
                )
                cmd_queue.put(
                    (
                        "POINT",
                        (p3, Color["blue"], 5),
                    )
                )

                area = (abs(point2.real - point1.real) + 1) * (
                    abs(point2.imag - point1.imag) + 1
                )
                logger.debug(f"Rectangle area: {area}")

                if area < max_area:
                    logger.debug(
                        f"Rectangle area {area} less than max area {max_area}, skipping rectangle"
                    )
                    continue

                for v in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
                    if vector_crosses_path(v[0], v[1], data):
                        logger.debug(
                            f"Rectangle edge {v[0]}->{v[1]} crosses the path, skipping rectangle"
                        )
                        break

                if point_in_path(p2, data) and point_in_path(p4, data):
                    cmd_queue.put(
                        (
                            "RECTANGLE",
                            (p1, p2, p3, p4, Color["green"], 2),
                        )
                    )
                    if area > max_area:
                        logger.debug(
                            f"New max rectangle found with area {area}, ({p1}, {p2}, {p3}, {p4})"
                        )
                        max_area = area
                        max_rectangle = (p1, p2, p3, p4)
                else:
                    cmd_queue.put(
                        (
                            "RECTANGLE",
                            (p1, p2, p3, p4, Color["red"], 2),
                        )
                    )
                time.sleep(0.01)  # Simulate some processing delay

            phase = None  # Empty
            logger.info("No more rectangles to process.")
            logger.info(
                f"Max rectangle area found: {max_area} with corners {max_rectangle}"
            )

        else:
            logger.info("No more phases to process, exiting game loop.")
            logger.info(
                f"Max rectangle area found: {max_area} with corners {max_rectangle}"
            )
            running = False

        time.sleep(0.01)  # Simulate some processing delay
        step = False

    return max_area


def vector_crosses_path(p1: complex, p2: complex, path: list[complex]) -> bool:
    """Return True if segment p1->p2 properly crosses the path.

    Rules:
    - Touching a vertex or sharing endpoints is NOT a crossing.
    - Colinear overlaps (vector lies on a path segment) are NOT crossings.
    - Only proper interior intersections count.
    """

    def on_segment(a: complex, b: complex, p: complex) -> bool:
        """Check if point p lies on segment a-b (inclusive)."""
        # Colinearity check via cross product == 0
        cross = (b.real - a.real) * (p.imag - a.imag) - (b.imag - a.imag) * (
            p.real - a.real
        )
        if cross != 0:
            return False
        # Within bounding box
        return min(a.real, b.real) <= p.real <= max(a.real, b.real) and min(
            a.imag, b.imag
        ) <= p.imag <= max(a.imag, b.imag)

    for i in range(len(path)):
        a = path[i]
        b = path[(i + 1) % len(path)]

        # Skip if the segment shares an endpoint with the vector
        if p1 == a or p1 == b or p2 == a or p2 == b:
            continue

        # If segments are colinear and overlap, treat as valid (not crossing)
        # Check if either vector endpoint lies on the path segment
        if on_segment(a, b, p1) or on_segment(a, b, p2):
            continue

        # Check for intersection between segments p1->p2 and a->b
        denom = (b.imag - a.imag) * (p2.real - p1.real) - (b.real - a.real) * (
            p2.imag - p1.imag
        )
        if denom == 0:
            # Parallel (or colinear but already handled by on_segment)
            continue

        ua = (
            (b.real - a.real) * (p1.imag - a.imag)
            - (b.imag - a.imag) * (p1.real - a.real)
        ) / denom
        ub = (
            (p2.real - p1.real) * (p1.imag - a.imag)
            - (p2.imag - p1.imag) * (p1.real - a.real)
        ) / denom

        # Proper interior intersection
        if 0 < ua < 1 and 0 < ub < 1:
            return True

    return False


def find_valid_diagonals(
    data: list[complex],
) -> Iterator[tuple[complex, complex, bool]]:
    """
    Check if a diagonal is valid.
    For every pair of point, check if the vector made by the two points is crossing the path
    """

    for i in range(len(data) - 1):
        for j in range(i + 1, len(data)):
            p1 = data[i]
            p2 = data[j]

            invalid = vector_crosses_path(p1, p2, data)
            yield (p1, p2, not invalid)


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
