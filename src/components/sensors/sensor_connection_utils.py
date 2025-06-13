from collections.abc import Callable

import networkx as nx

from src.components.sensors.sensor import Sensor
from src.components.sensors.sensor_manager import SensorManager
from src.components.sensors.sensor_math import euclid_distance


def udg_connection(distance: int) -> Callable[[Sensor, Sensor], bool]:
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
    def gg_connection_stub(
        sensor1: Sensor,
        sensor2: Sensor,
    ) -> bool:
        center_point = sensor1.position().mid_pos(sensor2.position())
        radius = sensor1.position().euclid_distance(center_point)
        for sensor in sensors:
            if sensor is sensor1 or sensor is sensor2:
                continue
            if sensor.position().euclid_distance(center_point) <= radius:
                return False
        return True

    return gg_connection_stub
