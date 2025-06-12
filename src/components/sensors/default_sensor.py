from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
import random
from typing import Any
import uuid

import pygame

from src.components.sensors.sensor import Cords, Sensor
from src.engine.geo_color import Colors
from src.engine.grid import PatchesGrid


class DefaultSensor(Sensor[float]):
    def __init__(
        self,
        cords: Cords,
        initial_state: dict[Any, Any] | None = None,
        on_receive: Callable[[DefaultSensor, list[float]], list[float]] | None = None,
        on_transmit: Callable[[DefaultSensor, list[float]], None] | None = None,
    ) -> None:
        super().__init__()
        self._id = uuid.uuid4()
        self._cords = cords
        self._current_color = Colors.CYAN
        self._on_receive = on_receive
        self._on_transmit = on_transmit

        self._message_queue: list[float] = []
        self._pending_message_queue: list[float] = []

        if initial_state is None:
            initial_state = {}
        self._state: dict[Any, Any] = deepcopy(initial_state)

    def id(self) -> uuid.UUID:
        return self._id

    def position(self) -> Cords:
        return self._cords

    def set_position(self, cords: Cords):
        self._cords = deepcopy(cords)

    def receive(self) -> list[float]:
        msgs = deepcopy(self._message_queue)
        if len(msgs) == 0:
            return []

        self._message_queue = []
        if self._on_receive is not None:
            return self._on_receive(self, msgs)
        return []

    def transmit(self, value: list[float]) -> None:
        if len(value) == 0:
            return

        if self._on_transmit is not None:
            self._on_transmit(self, deepcopy(value))

    def write_to_mem(self, value: list[float]) -> None:
        self._pending_message_queue += value

    def set_color(self, color: Colors):
        self._current_color = color

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: dict[Any, Any]):
        self._state = deepcopy(value)

    def _flush_run(self):
        self._message_queue = deepcopy(self._pending_message_queue)
        self._pending_message_queue = []

    def _draw(self, surface: pygame.Surface, offset: PatchesGrid) -> None:
        dot_radius = 5
        dot_color = self._current_color

        true_pos = offset.grid_to_pixel(int(self._cords.x), int(self._cords.y))
        pygame.draw.circle(surface, dot_color.to_tuple(), true_pos, dot_radius)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"DefualtSensor: \n\tid = {self._id}\n\tcords = {self._cords}"

    def __eq__(self, other: DefaultSensor) -> bool:
        if not isinstance(other, DefaultSensor):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)


def create_default_sensors(
    amount: int,
    grid: PatchesGrid,
    initial_state: dict[Any, Any] | None = None,
    on_receive: Callable[[DefaultSensor, list[float]], list[float]] | None = None,
    on_transmit: Callable[[DefaultSensor, list[float]], None] | None = None,
) -> list[DefaultSensor]:
    width = grid._grid_size - 1
    height = width

    cords = set()
    for _ in range(amount):
        current_cord = ()
        while current_cord in cords or current_cord == ():
            x = random.randint(0, width)
            y = random.randint(0, height)
            current_cord = (x, y)

        cords.add(current_cord)

    return [
        DefaultSensor(
            cords=Cords(cord[0], cord[1]),
            initial_state=initial_state,
            on_receive=on_receive,
            on_transmit=on_transmit,
        )
        for cord in cords
    ]
