from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
import random
from typing import Any, Generic, TypeVar
import uuid

import pygame

from src.components.coordinates import Coordinates
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


T = TypeVar("T")


class Sensor(Generic[T]):
    def __init__(
        self,
        cords: Coordinates,
        patches: PatchesGrid,
        initial_state: T = None,
        on_receive: Callable[[Sensor[T], list[float]], list[float]] = lambda _,
        value: value,
        on_transmit: Callable[[Sensor[T], list[float]], None] | None = None,
        on_measurement_change: Callable[[Sensor[T], Color], None] | None = None,
    ) -> None:
        super().__init__()
        self._id = uuid.uuid4()
        self._cords = cords
        self._grid = patches
        self._current_color = Color.CYAN
        self._on_receive = on_receive
        self._on_transmit = on_transmit
        self._on_measurement_change = on_measurement_change

        self._message_queue: list[float] = []
        self._pending_message_queue: list[float] = []

        self._state: T = deepcopy(initial_state)

        self._current_patch_color = self._grid.get_color(self._cords)
        self._neigbours: set[Sensor[T]] = set()
        self._marking_fn: Callable[[uuid.UUID, uuid.UUID], None] | None = None

    # =======================
    # Properties
    # =======================
    @property
    def id(self) -> uuid.UUID:
        return self._id

    @property
    def position(self) -> Coordinates:
        return self._cords

    @position.setter
    def set_position(self, cords: Coordinates) -> None:
        if not isinstance(cords, Coordinates):
            raise ValueError("you may only use Coordinates")
        self._cords = deepcopy(cords)

    @property
    def neighbours(self) -> set[Sensor[T]]:
        return self._neigbours

    @property
    def state(self) -> T:
        return self._state

    @state.setter
    def state(self, value: T):
        self._state = deepcopy(value)

    @property
    def color(self) -> Color:
        return self._current_color

    @color.setter
    def color(self, color: Color):
        if not isinstance(color, Color):
            raise ValueError("you may only use Color")
        self._current_color = color

    # =======================
    # Message passing
    # =======================
    def receive(self) -> list[float]:
        msgs = deepcopy(self._message_queue)
        if len(msgs) == 0:
            return []

        self._message_queue = []
        if self._on_receive is not None:
            return self._on_receive(self, msgs)
        return []

    def transmit(self, value: list[float]) -> None:
        if self._on_transmit is not None:
            self._on_transmit(self, deepcopy(value))

    def measurement_update(self, color: Color) -> None:
        if self._current_patch_color == color:
            return

        if self._on_measurement_change is not None:
            self._on_measurement_change(self, color)

        self._current_patch_color = deepcopy(color)

    def write_to_transmit_buffer(self, value: list[float]) -> None:
        self._pending_message_queue += value

    # =======================
    # DO NOT USE
    # =======================
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

    def __eq__(self, other: Sensor[T]) -> bool:
        if not isinstance(other, Sensor):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self.id)


def create_default_sensors(
    amount: int,
    grid: PatchesGrid,
    initial_state: Any = None,
    on_receive: Callable[[Sensor[T], list[float]], list[float]] = lambda _,
    value: value,
    on_transmit: Callable[[Sensor[T], list[float]], None] | None = None,
    on_measurement_change: Callable[[Sensor[T], Color], None] | None = None,
) -> list[Sensor[T]]:
    width = grid._grid_size - 1
    height = width

    coordinates = set()
    for _ in range(amount):
        current_cord = ()
        while current_cord in coordinates or current_cord == ():
            x = random.randint(0, width)
            y = random.randint(0, height)
            current_cord = (x, y)

        coordinates.add(current_cord)

    return [
        Sensor(
            cords=Coordinates(cord[0], cord[1]),
            patches=grid,
            initial_state=initial_state,
            on_receive=on_receive,
            on_transmit=on_transmit,
            on_measurement_change=on_measurement_change,
        )
        for cord in coordinates
    ]
