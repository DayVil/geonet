"""
Utility functions for creating and initializing sensors in the GeoNet framework.

This module provides convenient functions for creating multiple sensors with
randomized positions and configurations, simplifying the setup of sensor networks.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from src.components.coords.coordinate_utils import generate_random_coordinates
from src.components.sensors.sensor import Sensor
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


T = TypeVar("T")


def create_sensors(
    amount: int,
    grid: PatchesGrid,
    initial_state: T = None,
    on_receive: Callable[[Sensor[T], list[float]], None] | None = None,
    on_measurement_change: Callable[[Sensor[T], Color], None] | None = None,
) -> list[Sensor[T]]:
    """
    Create a specified number of sensors with random positions on the grid.

    This utility function creates multiple sensors and places them at random,
    non-overlapping positions on the grid.

    Args:
        amount (int): Number of sensors to create
        grid (PatchesGrid): The grid system to place sensors on
        initial_state (Any, optional): Initial state for all sensors. Defaults to None.
        on_receive (Callable, optional): Callback function for message reception.
            Function signature: (sensor, messages) -> None
        on_measurement_change (Callable, optional): Callback function for environmental
            changes. Function signature: (sensor, new_color) -> None

    Returns:
        list[Sensor[T]]: List of created sensors with random positions
    """
    coordinates = generate_random_coordinates(grid, amount)

    return [
        Sensor(
            cords=cord,
            patches=grid,
            initial_state=initial_state,
            on_receive=on_receive,
            on_measurement_change=on_measurement_change,
        )
        for cord in coordinates
    ]
