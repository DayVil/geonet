from collections.abc import Callable, Sequence
from itertools import combinations

import networkx as nx
import pygame

from src.components.sensor_math import euclid_distance
from src.engine.geo_color import Colors
from src.engine.grid import PatchesGrid

from .sensors.sensor import Sensor


class SensorManager:
    def __init__(self, grid: PatchesGrid) -> None:
        self._nx_graph = nx.Graph()
        self._grid = grid

    # =======================
    # Fetching Information
    # =======================
    def list_sensors(self) -> list[Sensor]:
        return [data["sensor"] for _, data in self._nx_graph.nodes(data=True)]

    def list_edges(self) -> list[tuple[Sensor, Sensor, dict]]:
        edges = []
        for sensor1_id, sensor2_id, edge_data in self._nx_graph.edges(data=True):
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]
            edges.append((sensor1, sensor2, edge_data))
        return edges

    def get_connected_sensors(self, sensor: Sensor) -> list[Sensor]:
        if sensor.id() not in self._nx_graph:
            return []

        connected_sensors = []
        for neighbor_id in self._nx_graph.neighbors(sensor.id()):
            neighbor_sensor = self._nx_graph.nodes[neighbor_id]["sensor"]
            connected_sensors.append(neighbor_sensor)

        return connected_sensors

    # =======================
    # Manipulationg Sensors
    # =======================
    def append_sensor(self, sensor: Sensor) -> None:
        if sensor.id() not in self._nx_graph:
            self._nx_graph.add_node(sensor.id(), sensor=sensor)

    def append_multiple_sensors(self, sensors: Sequence[Sensor]) -> None:
        for sensor in sensors:
            self.append_sensor(sensor)

    def connect_sensors(
        self,
        sensor1: Sensor,
        sensor2: Sensor,
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        if sensor1.id() not in self._nx_graph:
            self.append_sensor(sensor1)

        if sensor2.id() not in self._nx_graph:
            self.append_sensor(sensor2)

        if not self._nx_graph.has_edge(sensor1.id(), sensor2.id()):
            dist = distance_metric(sensor1, sensor2)
            self._nx_graph.add_edge(
                sensor1.id(),
                sensor2.id(),
                weight=dist,
                is_transmitting=False,
            )

    def connect_sensors_chain(
        self,
        sensors: Sequence[Sensor],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        sensor_buffer = list(sensors)
        if len(sensor_buffer) < 2:
            return

        prev_sensor = sensor_buffer.pop(0)
        while len(sensor_buffer) != 0:
            curr_sensor = sensor_buffer.pop(0)
            self.connect_sensors(prev_sensor, curr_sensor, distance_metric)
            prev_sensor = curr_sensor

    def connect_sensors_star(
        self,
        center_sensor: Sensor,
        sensors: Sequence[Sensor],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        sensor_buffer = list(sensors)
        if len(sensor_buffer) < 1:
            return

        for sensor in sensor_buffer:
            self.connect_sensors(center_sensor, sensor, distance_metric)

    def connect_sensors_if(
        self,
        sensors: Sequence[Sensor],
        condition: Callable[[Sensor, Sensor, Sequence[Sensor] | None], bool],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        for sensor1, sensor2 in combinations(sensors, 2):
            if condition(sensor1, sensor2, sensors):
                self.connect_sensors(sensor1, sensor2, distance_metric)

    # =======================
    # DO NOT USE
    # =======================
    def _mark_transmission(self, sender_id, receiver_id) -> None:
        """Mark that data transmission is occurring on this edge"""
        if self._nx_graph.has_edge(sender_id, receiver_id):
            self._nx_graph.edges[sender_id, receiver_id]["is_transmitting"] = True

    def _reset_transmissions(self) -> None:
        """Reset all transmission states"""
        for sensor1_id, sensor2_id in self._nx_graph.edges():
            self._nx_graph.edges[sensor1_id, sensor2_id]["is_transmitting"] = False

    def _draw(self, screen: pygame.Surface) -> None:
        for edge in self._nx_graph.edges():
            sensor1_id, sensor2_id = edge
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]
            edge_data = self._nx_graph.edges[sensor1_id, sensor2_id]

            pos1 = sensor1.position()
            pos2 = sensor2.position()

            pixel_pos1 = self._grid.grid_to_pixel(pos1.x, pos1.y)
            pixel_pos2 = self._grid.grid_to_pixel(pos2.x, pos2.y)

            is_transmitting = edge_data.get("is_transmitting", False)
            if is_transmitting:
                color = Colors.WHITE
                line_width = 4
            else:
                color = Colors.CONNECTION_GRAY
                line_width = 2

            pygame.draw.line(
                screen, color.to_tuple(), pixel_pos1, pixel_pos2, line_width
            )

        for sensor in self.list_sensors():
            sensor._draw(screen, self._grid)

    def _flush(self):
        for sensor in self.list_sensors():
            sensor._flush_run()

    def _update(self):
        self._flush()

        self._reset_transmissions()

        for sensor in self.list_sensors():
            data = sensor.read()
            connected_sensors = self.get_connected_sensors(sensor)
            for connected_sensor in connected_sensors:
                if len(data) > 0:
                    self._mark_transmission(sensor.id(), connected_sensor.id())
                    connected_sensor.write(data)
