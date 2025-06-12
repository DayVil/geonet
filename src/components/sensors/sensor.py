from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Any, Generic, TypeVar

import pygame

from src.engine.grid import PatchesGrid


T = TypeVar("T")


class Sensor(ABC, Generic[T]):
    @abstractmethod
    def id(self) -> Any:
        pass

    @abstractmethod
    def position(self) -> Cords:
        pass

    @abstractmethod
    def set_position(self, cords: Cords):
        pass

    @abstractmethod
    def receive(self) -> T:
        pass

    @abstractmethod
    def transmit(self, value: T) -> None:
        pass

    @abstractmethod
    def _flush_run(self):
        pass

    @abstractmethod
    def _draw(self, screen: pygame.Surface, offset: PatchesGrid) -> None:
        """Draws the instance of this sensor"""


@dataclass(frozen=True)
class Cords:
    x: int
    y: int

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def euclid_distance(self, other: Cords) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def mid_pos(self, other: Cords) -> Cords:
        return (self + other) // 2

    def __add__(self, other: Cords) -> Cords:
        return Cords(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Cords) -> Cords:
        return Cords(x=self.x - other.x, y=self.y - other.y)

    def __truediv__(self, scalar: float) -> Cords:
        return self.__floordiv__(scalar)

    def __floordiv__(self, scalar: float) -> Cords:
        return Cords(x=int(self.x / scalar), y=int(self.y / scalar))
