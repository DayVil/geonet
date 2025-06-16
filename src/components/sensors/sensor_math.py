"""
Mathematical operations and utilities for sensor networks.

This module provides mathematical functions commonly used in sensor network
simulations, including distance calculations and geometric operations.
"""

from typing import TypeVar

from src.components.sensors.sensor import Sensor


T = TypeVar("T")


def euclid_distance(sensor1: Sensor[T], sensor2: Sensor[T]) -> float:
    """
    Calculate the Euclidean distance between two sensors.

    This function computes the Euclidean distance between the positions of
    two sensors, which is commonly used for determining connectivity in
    sensor networks.

    Args:
        sensor1 (Sensor): The first sensor
        sensor2 (Sensor): The second sensor

    Returns:
        float: The Euclidean distance between the two sensor positions
    """
    pos1 = sensor1.position
    pos2 = sensor2.position
    return pos1.euclid_distance(pos2)
