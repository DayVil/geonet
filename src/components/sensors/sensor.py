from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import pygame

from src.components.coordinates import Cords
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
