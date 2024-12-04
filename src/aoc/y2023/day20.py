# Advent of Code 2023 - Day 20

from __future__ import annotations

import os
import queue
from enum import Enum
from typing import Protocol

import networkx as nx
from pyvis.network import Network

from aoc.utils import read_input


class Pulse(Enum):
    HIGH = 1
    LOW = 0


class Module(Protocol):
    name: str
    dest: list[str]

    def process_signal(self, parent: str, signal: Pulse) -> None: ...


class Rx:
    name: str
    dest: list[str]

    def __init__(self) -> None:
        self.name = "rx"
        self.dest = []

    def process_signal(self, parent: str, signal: Pulse) -> None:
        # print(f"{self.name}: Received {signal} from {parent}")
        pass

    def __str__(self) -> str:
        return f"{self.name}: {self.dest}"


class Button:
    name: str
    dest: list[str]

    def __init__(self) -> None:
        self.name = "Button"
        self.dest = ["Broadcaster"]

    def process_signal(self, parent: str, signal: Pulse) -> None:  # noqa
        # print(f"{self.name}: Sending {signal} to {self.dest}")
        for dest in self.dest:
            PULSES.put([self.name, dest, signal])

    def __str__(self) -> str:
        return f"{self.name}: {self.dest}"


class Broadcaster:
    name: str
    dest: list[str]

    def __init__(self, dest: str) -> None:
        self.name = "Broadcaster"
        self.dest = dest.split(", ")

    def process_signal(self, parent: str, signal: Pulse) -> None:  # noqa
        # print(f"{self.name}: Broadcasting {signal} to {self.dest}")
        for dest in self.dest:
            PULSES.put([self.name, dest, signal])

    def __str__(self) -> str:
        return f"{self.name}: {self.dest}"


class FilpFlop:
    name: str
    dest: list[str]
    _is_on: bool = False

    def is_on(self) -> bool:
        return self._is_on

    def is_off(self) -> bool:
        return not self._is_on

    def state(self) -> str:
        return "on" if self.is_on() else "off"

    def __init__(self, name: str, dest: str) -> None:
        self.name = name[1:]
        self.dest = dest.split(", ")

    def process_signal(self, parent: str, signal: Pulse) -> None:  # noqa
        # Ignore high signals
        if signal == Pulse.HIGH:
            # Ignore the signal
            # print(f"{self.name}: Ignoring high signal from {parent} because FlipFlop is {self.state()}")
            return

        if self.is_off():
            # Switch was off, sends a high pulse to the destinations
            # print(f"{self.name}: {self.state()} -> Sendiing high pulse to {self.dest}")
            for dest in self.dest:
                PULSES.put([self.name, dest, Pulse.HIGH])
        else:
            # Switch was on, sends a low pulse to the destinations
            # print(f"{self.name}: {self.state()} -> Sendiing low pulse to {self.dest}")
            for dest in self.dest:
                PULSES.put([self.name, dest, Pulse.LOW])

        # Switch On/Off on low signals
        self._is_on = not self._is_on

    def __str__(self) -> str:
        return f"{self.name}: {self.state()} - {self.dest}"


class Conjonction:
    name: str
    dest: list[str]
    recent_pulses: dict[str, Pulse]

    def __init__(self, name: str, dest: str) -> None:
        self.name = name[1:]
        self.dest = dest.split(", ")
        self.recent_pulses = {}

    def process_signal(self, parent: str, signal: Pulse) -> None:
        # Update pulse memory
        self.recent_pulses[parent] = signal

        if all(pulse == Pulse.HIGH for pulse in self.recent_pulses.values()):
            # All inputs are high, send a low pulse to the destinations
            # print(f"{self.name}: Sending low pulse to {self.dest}")
            for dest in self.dest:
                PULSES.put([self.name, dest, Pulse.LOW])
        else:
            # At least one input is low, send a high pulse to the destinations
            # print(f"{self.name}: Sending high pulse to {self.dest}")
            for dest in self.dest:
                PULSES.put([self.name, dest, Pulse.HIGH])
        # print(f"{self.name}: {self.recent_pulses}")

    def __str__(self) -> str:
        return f"{self.name}: {dict(self.recent_pulses)} - {self.dest}"


PULSES = queue.Queue()
MODULES: dict[str, Module] = {}
NETWORK: nx.DiGraph = nx.DiGraph()


def get_input_data() -> list[str]:
    return read_input(day=20, year=2023)


def parse_module(line: str) -> Module:
    name, dest = line.rstrip().split(" -> ")
    if name == "broadcaster":
        return Broadcaster(dest)

    if name.startswith("%"):
        return FilpFlop(name, dest)

    if name.startswith("&"):
        return Conjonction(name, dest)

    _msg = f"Unknown module: {name}"
    raise ValueError(_msg)


def parse_input(data: list[str]) -> None:
    for line in data:
        module = parse_module(line)
        MODULES[module.name] = module

    MODULES["rx"] = Rx()
    MODULES["Button"] = Button()


def build_network() -> None:
    # Build Vertices
    NETWORK.add_nodes_from(MODULES.keys())
    NETWORK.add_nodes_from(["Button", "rx"])

    # Build Edges
    for module in MODULES.values():
        for dest in module.dest:
            NETWORK.add_edge(module.name, dest)

    NETWORK.add_edge("Button", "Broadcaster")


def display_network() -> None:
    g = Network(directed=True)
    g.from_nx(NETWORK)
    g.prep_notebook()
    g.show("data/network.html")
    cmd = "open data/network.html"
    os.system(cmd)  # noqa


def init_conjonction_modules() -> None:
    for module in MODULES.values():
        if isinstance(module, Conjonction):
            # Retrieve module parents
            parents = NETWORK.predecessors(module.name)
            for parent in parents:
                # Send a low pulse to the module
                module.recent_pulses[parent] = Pulse.LOW


def get_test_input_data() -> list[str]:
    data = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx"""
    return data.split("\n")


def init(data: list[str]) -> None:
    parse_input(data)

    # Build network
    build_network()

    # Inititalize Conjonction Modules
    init_conjonction_modules()

    # Show network
    # display_network()


def part1() -> int:
    data = get_input_data()

    init(data)

    # Par Modules

    nb_high = 0
    nb_low = 0

    for _ in range(1000):
        # Send a high pulse to the Button
        PULSES.put(["Button", "Broadcaster", Pulse.LOW])

        # Process pulses
        while PULSES.qsize() > 0:
            source, dest, pulse = PULSES.get()
            if pulse == Pulse.HIGH:
                nb_high += 1
            else:
                nb_low += 1

            # print(f"Processing {type(MODULES[dest]).__name__!s:<15} {source}  - {pulse} -> {dest}")

            MODULES[dest].process_signal(source, pulse)
            # print(f"Queue: {PULSES.qsize()}")

    return nb_high * nb_low


def count_pulses(f_src: str, f_dest: str, f_pulse: Pulse) -> int:
    for nb_press in range(1, 50000):
        PULSES.put(["Button", "Broadcaster", Pulse.LOW])

        while PULSES.qsize() > 0:
            source, dest, pulse = PULSES.get()

            if source == f_src and dest == f_dest and pulse == f_pulse:
                # print(f"Found: {source} -> {dest} : {pulse}, after {nb_press} presses")
                return nb_press

            MODULES[dest].process_signal(source, pulse)
    return 0


def part2() -> int:
    data = get_input_data()
    init(data)

    # display_network()

    # How many inputs to get fg to send a high pulse to vr
    vr_p = count_pulses("fg", "vr", Pulse.HIGH)
    # print(f"fg -> vr: {vr_p}")
    init(data)
    # How many inputs to get pq to send a high pulse to vr
    pq_p = count_pulses("pq", "vr", Pulse.HIGH)
    # print(f"pq -> vr: {pq_p}")
    init(data)
    # How many inputs to get fm to send a high pulse to vr
    fm_p = count_pulses("fm", "vr", Pulse.HIGH)
    # print(f"fm -> vr: {fm_p}")
    init(data)
    # How many inputs to get dk to send a high pulse to vr
    dk_p = count_pulses("dk", "vr", Pulse.HIGH)
    # print(f"dk -> vr: {dk_p}")

    return vr_p * pq_p * fm_p * dk_p
