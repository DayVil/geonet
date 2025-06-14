from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def euclid_distance(self, other: Coordinates) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def mid_pos(self, other: Coordinates) -> Coordinates:
        return Coordinates(x=(self.x + other.x) / 2, y=(self.y + other.y) / 2)

    def __add__(self, other: Coordinates) -> Coordinates:
        return Coordinates(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Coordinates) -> Coordinates:
        return Coordinates(x=self.x - other.x, y=self.y - other.y)

    def __truediv__(self, scalar: float) -> Coordinates:
        return Coordinates(x=self.x / scalar, y=self.y / scalar)

    def __floordiv__(self, scalar: float) -> Coordinates:
        return Coordinates(x=self.x // scalar, y=self.y // scalar)
