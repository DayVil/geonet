from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Cords:
    x: float
    y: float

    def to_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def euclid_distance(self, other: Cords) -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def mid_pos(self, other: Cords) -> Cords:
        return Cords(x=(self.x + other.x) / 2, y=(self.y + other.y) / 2)

    def __add__(self, other: Cords) -> Cords:
        return Cords(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Cords) -> Cords:
        return Cords(x=self.x - other.x, y=self.y - other.y)

    def __truediv__(self, scalar: float) -> Cords:
        return Cords(x=self.x / scalar, y=self.y / scalar)

    def __floordiv__(self, scalar: float) -> Cords:
        return Cords(x=self.x // scalar, y=self.y // scalar)
