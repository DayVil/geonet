from collections.abc import Callable

import networkx as nx

from src.components.sensors.sensor import Sensor
from src.components.sensors.sensor_manager import SensorManager
from src.components.sensors.sensor_math import euclid_distance


def udg_connection(distance: int) -> Callable[[Sensor, Sensor], bool]:
    """
    Create a Unit Disk Graph (UDG) connection function.

    Returns a connection function that considers two sensors connected if they
    are within the specified distance of each other. This is a common model
    for wireless sensor networks where sensors have a fixed communication range.

    Args:
        distance (int): Maximum distance for sensor connectivity

    Returns:
        Callable[[Sensor, Sensor], bool]: A function that returns True if two
            sensors should be connected based on the distance criterion
    """
    internal_distance = distance

    def udg_connection_stub(
        sensor1: Sensor,
        sensor2: Sensor,
    ) -> bool:
        if euclid_distance(sensor1, sensor2) <= internal_distance:
            return True
        return False

    return udg_connection_stub


def udg_connection_autotune(
    manager: SensorManager, sensors: list[Sensor]
) -> Callable[[Sensor, Sensor], bool]:
    """
    Create an auto-tuned UDG connection function based on network connectivity.

    This function analyzes the minimum spanning tree of a fully connected sensor
    network to determine the optimal connection distance. It ensures network
    connectivity while minimizing the connection range.

    Args:
        manager (SensorManager): The sensor manager to use for network analysis
        sensors (list[Sensor]): List of sensors to analyze

    Returns:
        Callable[[Sensor, Sensor], bool]: A function that returns True if two
            sensors should be connected based on the auto-tuned distance criterion
    """
    manager.connect_sensors_mesh(sensors)
    network = manager._nx_graph
    mst = nx.minimum_spanning_tree(network)
    mst_edges = list(mst.edges(data=True))
    edges_weight = [data["weight"] for _, _, data in list(mst_edges)]
    len_required = max(edges_weight)
    manager.disconnect_multiple_sensors(sensors)

    def udg_connection_stub(
        sensor1: Sensor,
        sensor2: Sensor,
    ) -> bool:
        if euclid_distance(sensor1, sensor2) <= len_required:
            return True
        return False

    return udg_connection_stub


def gg_connection(sensors: list[Sensor]) -> Callable[[Sensor, Sensor], bool]:
    """
    Create a Gabriel Graph (GG) connection function.

    In a Gabriel Graph, two sensors are connected if no other sensor lies within
    the circle that has the line segment between the two sensors as its diameter.
    This creates a sparse connectivity pattern while maintaining network connectivity.

    Args:
        sensors (list[Sensor]): List of all sensors in the network (needed to
            check for interference from other sensors)

    Returns:
        Callable[[Sensor, Sensor], bool]: A function that returns True if two
            sensors should be connected based on the Gabriel Graph criterion
    """

    def gg_connection_stub(
        sensor1: Sensor,
        sensor2: Sensor,
    ) -> bool:
        center_point = sensor1.position.mid_pos(sensor2.position)
        radius = sensor1.position.euclid_distance(center_point)
        for sensor in sensors:
            if sensor is sensor1 or sensor is sensor2:
                continue
            if sensor.position.euclid_distance(center_point) <= radius:
                return False
        return True

    return gg_connection_stub
