from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
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
    def read(self) -> T:
        pass

    @abstractmethod
    def write(self, value: T) -> None:
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
