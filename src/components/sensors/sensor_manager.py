from __future__ import annotations

from collections.abc import Callable, Sequence
from copy import deepcopy
from itertools import combinations
from typing import Any
import uuid

import networkx as nx
import pygame

from src.components.sensors.sensor import Sensor
from src.components.sensors.sensor_math import euclid_distance
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


class SensorManager:
    """
    Manages a collection of sensors and their network connections.

    This class provides comprehensive management of sensor networks, including
    sensor registration, connection management, network topology creation,
    visualization, and simulation updates. It uses NetworkX for efficient
    graph operations and provides various connectivity patterns.

    Attributes:
        _nx_graph (nx.Graph): NetworkX graph representing the sensor network
        _grid (PatchesGrid): Reference to the grid system
    """

    # =======================
    # Initialization
    # =======================
    def __init__(self, grid: PatchesGrid) -> None:
        """
        Initialize the sensor manager with a grid system.

        Args:
            grid (PatchesGrid): The grid system to manage sensors on
        """
        self._nx_graph = nx.Graph()
        self._grid = grid

    # =======================
    # Information retrieval methods
    # =======================
    def list_sensors(self) -> list[Sensor]:
        """
        Get a list of all sensors managed by this manager.

        Returns:
            list[Sensor]: List of all sensors in the network
        """
        return [data["sensor"] for _, data in self._nx_graph.nodes(data=True)]

    def list_edges(self) -> list[tuple[Sensor, Sensor, dict]]:
        """
        Get a list of all connections between sensors.

        Returns:
            list[tuple[Sensor, Sensor, dict]]: List of tuples containing
                (sensor1, sensor2, edge_data) for each connection
        """
        edges = []
        for sensor1_id, sensor2_id, edge_data in self._nx_graph.edges(data=True):
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]
            edges.append((sensor1, sensor2, edge_data))
        return edges

    def get_connected_sensors(self, sensor: Sensor) -> list[Sensor]:
        """
        Get all sensors directly connected to a given sensor.

        Args:
            sensor (Sensor): The sensor to find neighbors for

        Returns:
            list[Sensor]: List of sensors connected to the given sensor
        """
        if sensor.id not in self._nx_graph:
            return []

        connected_sensors = []
        for neighbor_id in self._nx_graph.neighbors(sensor.id):
            neighbor_sensor = self._nx_graph.nodes[neighbor_id]["sensor"]
            connected_sensors.append(neighbor_sensor)

        return connected_sensors

    # =======================
    # Sensor management methods
    # =======================
    def append_sensor(self, sensor: Sensor) -> None:
        """
        Add a sensor to the network.

        Args:
            sensor (Sensor): The sensor to add to the network
        """
        if sensor.id not in self._nx_graph:
            sensor._sensor_manager = self
            self._nx_graph.add_node(sensor.id, sensor=sensor)

    def append_multiple_sensors(self, sensors: Sequence[Sensor]) -> None:
        """
        Add multiple sensors to the network.

        Args:
            sensors (Sequence[Sensor]): Collection of sensors to add
        """
        for sensor in sensors:
            self.append_sensor(sensor)

    # =======================
    # Connection management methods
    # =======================
    def connect_sensors(
        self,
        sensor1: Sensor,
        sensor2: Sensor,
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        """
        Create a connection between two sensors.

        Args:
            sensor1 (Sensor): First sensor to connect
            sensor2 (Sensor): Second sensor to connect
            distance_metric (Callable, optional): Function to calculate distance
                between sensors. Defaults to euclid_distance.
        """
        if sensor1.id not in self._nx_graph:
            self.append_sensor(sensor1)

        if sensor2.id not in self._nx_graph:
            self.append_sensor(sensor2)

        if not self._nx_graph.has_edge(sensor1.id, sensor2.id):
            dist = distance_metric(sensor1, sensor2)
            self._nx_graph.add_edge(
                sensor1.id,
                sensor2.id,
                weight=dist,
                is_transmitting=False,
            )
            sensor1._neighbour.add(sensor2)
            sensor2._neighbour.add(sensor1)

    def disconnect_sensors(self, sensor1: Sensor, sensor2: Sensor) -> None:
        """
        Remove the connection between two sensors.

        Args:
            sensor1 (Sensor): First sensor to disconnect
            sensor2 (Sensor): Second sensor to disconnect
        """
        if sensor1.id not in self._nx_graph:
            self.append_sensor(sensor1)

        if sensor2.id not in self._nx_graph:
            self.append_sensor(sensor2)

        self._nx_graph.remove_edge(sensor1.id, sensor2.id)
        sensor1._neighbour.remove(sensor2)
        sensor2._neighbour.remove(sensor1)

    def disconnect_multiple_sensors(self, sensors: Sequence[Sensor]) -> None:
        """
        Remove all connections between a group of sensors.

        Args:
            sensors (Sequence[Sensor]): Collection of sensors to disconnect from each other
        """
        for sensor1, sensor2 in combinations(sensors, 2):
            self.disconnect_sensors(sensor1, sensor2)

    # =======================
    # Network topology creation methods
    # =======================
    def connect_sensors_mesh(
        self,
        sensors: Sequence[Sensor],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        """
        Connect all sensors to each other in a full mesh topology.

        Creates a complete graph where every sensor is connected to every other
        sensor. This provides maximum connectivity but high network overhead.

        Args:
            sensors (Sequence[Sensor]): Collection of sensors to connect
            distance_metric (Callable, optional): Function to calculate distance
                between sensors. Defaults to euclid_distance.
        """
        for sensor1, sensor2 in combinations(sensors, 2):
            self.connect_sensors(sensor1, sensor2, distance_metric)

    def connect_sensors_chain(
        self,
        sensors: Sequence[Sensor],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        """
        Connect sensors in a linear chain topology.

        Creates a path graph where sensors are connected in sequence. This
        provides minimal connectivity with potential for network partitioning.

        Args:
            sensors (Sequence[Sensor]): Collection of sensors to connect in sequence
            distance_metric (Callable, optional): Function to calculate distance
                between sensors. Defaults to euclid_distance.
        """
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
        """
        Connect sensors in a star topology with a central hub.

        Creates a star graph where one central sensor is connected to all others.
        This provides a single point of failure but efficient centralized communication.

        Args:
            center_sensor (Sensor): The sensor to use as the central hub
            sensors (Sequence[Sensor]): Collection of sensors to connect to the center
            distance_metric (Callable, optional): Function to calculate distance
                between sensors. Defaults to euclid_distance.
        """
        sensor_buffer = list(sensors)
        if len(sensor_buffer) < 1:
            return

        for sensor in sensor_buffer:
            self.connect_sensors(center_sensor, sensor, distance_metric)

    def connect_sensors_if(
        self,
        sensors: Sequence[Sensor],
        condition: Callable[[Sensor, Sensor], bool],
        distance_metric: Callable[[Sensor, Sensor], float] = euclid_distance,
    ) -> None:
        """
        Connect sensors based on a custom condition function.

        This method allows for flexible connection patterns by evaluating a
        condition function for each pair of sensors.

        Args:
            sensors (Sequence[Sensor]): Collection of sensors to evaluate
            condition (Callable[[Sensor, Sensor], bool]): Function that returns
                True if two sensors should be connected
            distance_metric (Callable, optional): Function to calculate distance
                between sensors. Defaults to euclid_distance.
        """
        for sensor1, sensor2 in combinations(sensors, 2):
            if condition(sensor1, sensor2):
                self.connect_sensors(sensor1, sensor2, distance_metric)

    # =======================
    # Internal methods - DO NOT USE directly
    # =======================
    def _mark_transmission(self, sender_id: uuid.UUID, receiver_id: uuid.UUID) -> None:
        """
        Mark that data transmission is occurring on a connection.

        This internal method is used for visualization purposes to highlight
        active communication links.

        Args:
            sender_id (uuid.UUID): ID of the sending sensor
            receiver_id (uuid.UUID): ID of the receiving sensor
        """
        if self._nx_graph.has_edge(sender_id, receiver_id):
            self._nx_graph.edges[sender_id, receiver_id]["is_transmitting"] = True

    def _reset_transmissions(self) -> None:
        """
        Reset all transmission states for the next simulation step.

        This internal method clears transmission markers for visualization.
        """
        for sensor1_id, sensor2_id in self._nx_graph.edges():
            self._nx_graph.edges[sensor1_id, sensor2_id]["is_transmitting"] = False

    def _draw(self, screen: pygame.Surface) -> None:
        """
        Draw the sensor network on the pygame surface.

        This internal method renders all sensors and their connections, with
        special highlighting for active transmissions.

        Args:
            screen (pygame.Surface): The surface to draw on
        """
        for edge in self._nx_graph.edges():
            sensor1_id, sensor2_id = edge
            sensor1 = self._nx_graph.nodes[sensor1_id]["sensor"]
            sensor2 = self._nx_graph.nodes[sensor2_id]["sensor"]
            edge_data = self._nx_graph.edges[sensor1_id, sensor2_id]

            pos1 = sensor1.position
            pos2 = sensor2.position

            pixel_pos1 = self._grid.grid_to_pixel(pos1.x, pos1.y)
            pixel_pos2 = self._grid.grid_to_pixel(pos2.x, pos2.y)

            is_transmitting = edge_data.get("is_transmitting", False)
            if is_transmitting:
                color = Color.WHITE
                line_width = 4
            else:
                color = Color.CONNECTION_GRAY
                line_width = 2

            pygame.draw.line(
                screen, color.to_tuple(), pixel_pos1, pixel_pos2, line_width
            )

        for sensor in self.list_sensors():
            sensor._draw(screen, self._grid)

    def _flush(self):
        """
        Flush message queues for all sensors.

        This internal method processes pending messages for all sensors.
        """
        for sensor in self.list_sensors():
            sensor._flush_run()

    def _update(
        self,
        update_fn: Callable[[Any], Any],
        global_state: Any,
    ):
        """
        Update the sensor network simulation state.

        This internal method coordinates the simulation update process,
        including message processing, environmental sensing, and user-defined
        update logic.

        Args:
            update_fn (Callable[[Any], Any]): User-defined update function
            global_state (Any): Current global state of the simulation

        Returns:
            Any: Updated global state
        """
        self._flush()
        self._reset_transmissions()

        for sensor in self.list_sensors():
            cell_color = self._grid.get_color(sensor.position)
            sensor.measurement_update(cell_color)
            sensor._receive()

        new_global_state = update_fn(global_state)
        return deepcopy(new_global_state)
