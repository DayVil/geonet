from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Coordinates:
    """
    A dataclass representing 2D coordinates with common mathematical operations.

    This immutable class provides coordinate-based operations commonly used in
    sensor networks and grid-based systems.

    Attributes:
        x (float): The x-coordinate value
        y (float): The y-coordinate value
    """

    x: float
    y: float

    def to_tuple(self) -> tuple[float, float]:
        """
        Convert coordinates to a tuple representation.

        Returns:
            tuple[float, float]: A tuple containing (x, y) values
        """
        return (self.x, self.y)

    def euclid_distance(self, other: Coordinates) -> float:
        """
        Calculate the Euclidean distance between this point and another.

        Args:
            other (Coordinates): The other coordinate point

        Returns:
            float: The Euclidean distance between the two points
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def mid_pos(self, other: Coordinates) -> Coordinates:
        """
        Calculate the midpoint between this coordinate and another.

        Args:
            other (Coordinates): The other coordinate point

        Returns:
            Coordinates: A new Coordinates object representing the midpoint
        """
        return Coordinates(x=(self.x + other.x) / 2, y=(self.y + other.y) / 2)

    def __add__(self, other: Coordinates) -> Coordinates:
        """
        Add two coordinates together (vector addition).

        Args:
            other (Coordinates): The coordinate to add

        Returns:
            Coordinates: A new coordinate with added values
        """
        return Coordinates(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Coordinates) -> Coordinates:
        """
        Subtract one coordinate from another (vector subtraction).

        Args:
            other (Coordinates): The coordinate to subtract

        Returns:
            Coordinates: A new coordinate with subtracted values
        """
        return Coordinates(x=self.x - other.x, y=self.y - other.y)

    def __truediv__(self, scalar: float) -> Coordinates:
        """
        Divide coordinates by a scalar value (true division).

        Args:
            scalar (float): The scalar value to divide by

        Returns:
            Coordinates: A new coordinate with divided values
        """
        return Coordinates(x=self.x / scalar, y=self.y / scalar)

    def __floordiv__(self, scalar: float) -> Coordinates:
        """
        Divide coordinates by a scalar value (floor division).

        Args:
            scalar (float): The scalar value to divide by

        Returns:
            Coordinates: A new coordinate with floor-divided values
        """
        return Coordinates(x=self.x // scalar, y=self.y // scalar)
