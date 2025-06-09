from collections.abc import Callable
from copy import deepcopy

from icecream import ic
import networkx as nx
import pygame

from src.engine.geo_color import Colors
from src.engine.grid import Grid

from .sensors.sensor import Sensor


class SensorManager:
    def __init__(self) -> None:
        self._nx_graph = nx.Graph()

    def list_sensors(self) -> list[Sensor]:
        return [data["sensor"] for _, data in self._nx_graph.nodes(data=True)]

    def list_edges(self) -> list[tuple[Sensor, Sensor, dict]]:
        edges = []
        for sensor1_id, sensor2_id, edge_data in self._nx_graph.edges(data=True):
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]
            edges.append((sensor1, sensor2, edge_data))
        return edges

    def append_sensor(self, sensor: Sensor) -> Sensor:
        if sensor.id() not in self._nx_graph:
            sensor = deepcopy(sensor)
            self._nx_graph.add_node(sensor.id(), sensor=sensor)

        return sensor

    def connect_sensors(
        self,
        sensor1: Sensor,
        sensor2: Sensor,
        distance_metric: Callable[[Sensor, Sensor], float],
    ) -> None:
        if sensor1.id() not in self._nx_graph:
            sensor1 = self.append_sensor(sensor1)

        if sensor2.id() not in self._nx_graph:
            sensor2 = self.append_sensor(sensor2)

        if not self._nx_graph.has_edge(sensor1.id(), sensor2.id()):
            dist = distance_metric(sensor1, sensor2)
            self._nx_graph.add_edge(sensor1.id(), sensor2.id(), weigth=dist)

    def get_connected_sensors(self, sensor: Sensor) -> list[Sensor]:
        if sensor.id() not in self._nx_graph:
            return []

        connected_sensors = []
        for neighbor_id in self._nx_graph.neighbors(sensor.id()):
            neighbor_sensor = self._nx_graph.nodes[neighbor_id]["sensor"]
            connected_sensors.append(neighbor_sensor)

        return connected_sensors

    def _draw(self, screen: pygame.Surface, offset: Grid) -> None:
        for edge in self._nx_graph.edges():
            sensor1_id, sensor2_id = edge
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]

            pos1 = sensor1.position()
            pos2 = sensor2.position()

            pixel_pos1 = offset.grid_to_pixel(pos1.x, pos1.y)
            pixel_pos2 = offset.grid_to_pixel(pos2.x, pos2.y)

            pygame.draw.line(screen, Colors.WHITE, pixel_pos1, pixel_pos2, 2)

        for sensor in self.list_sensors():
            sensor._draw(screen, offset)

    def _flush(self):
        for sensor in self.list_sensors():
            sensor._flush_run()

    def _update(self):
        # First flush all pending messages to make them available for reading
        self._flush()

        for sensor in self.list_sensors():
            data = sensor.read()
            if len(data) != 0:
                ic(data)
            connected_sensors = self.get_connected_sensors(sensor)
            for connected_sensor in connected_sensors:
                connected_sensor.write(data)
