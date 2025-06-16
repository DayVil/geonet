# pyright: reportPrivateUsage=false

from __future__ import annotations

import random

from src.components.coords.coordinates import Coordinates
from src.engine.grid import PatchesGrid


def generate_random_coordinates(
    patches: PatchesGrid, amount: int = 1
) -> list[Coordinates]:
    """
    Generate a list of random coordinates within the given grid.

    Args:
        patches (PatchesGrid): The grid system to generate coordinates within
        amount (int): Number of coordinates to generate (default: 1)

    Returns:
        list[Coordinates]: List of unique random coordinates

    Raises:
        AssertionError: If amount is negative
    """
    if amount < 0:
        raise ValueError("Amount may not be negative")

    width = patches._grid_size - 1
    height = width

    coordinates: set[Coordinates] = set()
    for _ in range(amount):
        current_cord: Coordinates | None = None
        while current_cord in coordinates or current_cord is None:
            x = random.randint(0, width)
            y = random.randint(0, height)
            current_cord = Coordinates(x, y)

        coordinates.add(current_cord)

    return list(coordinates)


def generate_random_coordinate(patches: PatchesGrid) -> Coordinates:
    """
    Generate a single random coordinate within the given grid.

    Args:
        patches (PatchesGrid): The grid system to generate coordinates within

    Returns:
        Coordinates: A single random coordinate
    """
    return generate_random_coordinates(patches, 1)[0]
