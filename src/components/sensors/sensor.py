from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
import random
from typing import TYPE_CHECKING, Any, Generic, TypeVar
import uuid

import pygame

from src.components.coordinates import Coordinates
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


if TYPE_CHECKING:
    from src.components.sensors.sensor_manager import SensorManager


T = TypeVar("T")


class Sensor(Generic[T]):
    """
    A generic sensor class for sensor network simulations.

    This class represents a sensor in a wireless sensor network. Each sensor has
    a position on the grid, can communicate with neighboring sensors, maintains
    internal state, and can respond to environmental changes through callbacks.

    Type Parameters:
        T: The type of the internal state maintained by the sensor

    Attributes:
        _id (uuid.UUID): Unique identifier for the sensor
        _cords (Coordinates): Position of the sensor on the grid
        _grid (PatchesGrid): Reference to the grid system
        _current_color (Color): Color used to display the sensor
        _on_receive (Callable | None): Callback function for receiving messages
        _on_measurement_change (Callable | None): Callback for environmental changes
        _message_queue (list[float]): Queue of received messages to process
        _pending_message_queue (list[float]): Buffer for incoming messages
        _state (T): Internal state of the sensor
        _current_patch_color (Color): Current color of the grid patch the sensor is on
        _neighbour (set[Sensor]): Set of neighboring sensors
        _sensor_manager (SensorManager | None): Reference to the sensor manager
    """

    # =======================
    # Initialization
    # =======================
    def __init__(
        self,
        cords: Coordinates,
        patches: PatchesGrid,
        initial_state: T = None,
        on_receive: Callable[[Sensor[T], list[float]], None] | None = None,
        on_measurement_change: Callable[[Sensor[T], Color], None] | None = None,
    ) -> None:
        """
        Initialize a new sensor.

        Args:
            cords (Coordinates): Position of the sensor on the grid
            patches (PatchesGrid): Reference to the grid system
            initial_state (T, optional): Initial internal state. Defaults to None.
            on_receive (Callable, optional): Callback function called when messages
                are received. Function signature: (sensor, messages) -> None
            on_measurement_change (Callable, optional): Callback function called when
                the environment changes. Function signature: (sensor, new_color) -> None
        """
        super().__init__()
        self._id = uuid.uuid4()
        self._cords = cords
        self._grid = patches
        self._current_color = Color.CYAN
        self._on_receive = on_receive
        self._on_measurement_change = on_measurement_change

        self._message_queue: list[float] = []
        self._pending_message_queue: list[float] = []

        self._state: T = deepcopy(initial_state)
        self._current_patch_color = self._grid.get_color(self._cords)

        self._neighbour: set[Sensor] = set()

        self._sensor_manager: SensorManager | None = None

    # =======================
    # Properties - sensor information access
    # =======================
    @property
    def id(self) -> uuid.UUID:
        """
        Get the unique identifier of the sensor.

        Returns:
            uuid.UUID: The sensor's unique identifier
        """
        return self._id

    @property
    def position(self) -> Coordinates:
        """
        Get the current position of the sensor.

        Returns:
            Coordinates: The sensor's position on the grid
        """
        return self._cords

    @position.setter
    def set_position(self, cords: Coordinates) -> None:
        """
        Set the position of the sensor.

        Args:
            cords (Coordinates): New position for the sensor

        Raises:
            ValueError: If cords is not a Coordinates instance
        """
        if not isinstance(cords, Coordinates):
            raise ValueError("you may only use Coordinates")
        self._cords = deepcopy(cords)

    @property
    def neighbours(self) -> list[Sensor[T]]:
        """
        Get the list of neighboring sensors.

        Returns:
            list[Sensor[T]]: List of sensors connected to this sensor
        """
        return list(self._neighbour)

    @property
    def state(self) -> T:
        """
        Get the current internal state of the sensor.

        Returns:
            T: The sensor's internal state
        """
        return self._state

    @state.setter
    def state(self, value: T):
        """
        Set the internal state of the sensor.

        Args:
            value (T): New state value
        """
        self._state = deepcopy(value)

    @property
    def color(self) -> Color:
        """
        Get the display color of the sensor.

        Returns:
            Color: The color used to render the sensor
        """
        return self._current_color

    @color.setter
    def color(self, color: Color):
        """
        Set the display color of the sensor.

        Args:
            color (Color): New color for the sensor

        Raises:
            ValueError: If color is not a Color instance
        """
        if not isinstance(color, Color):
            raise ValueError("you may only use Color")
        self._current_color = color

    # =======================
    # Communication methods
    # =======================
    def transmit(self, to_sensor: Sensor, values: list[float]) -> None:
        """
        Send a message to a specific sensor.

        Args:
            to_sensor (Sensor): The target sensor to send the message to
            values (list[float]): List of numerical values to transmit
        """
        if len(values) == 0:
            return

        if self._sensor_manager is not None:
            self._sensor_manager._mark_transmission(self.id, to_sensor.id)
        to_sensor._write_to_transmit_buffer(values)

    def broadcast(self, values: list[float] | list[float]):
        """
        Broadcast a message to all neighboring sensors.

        Args:
            values (list[float]): List of numerical values to broadcast
        """
        for neighbour in self.neighbours:
            self.transmit(neighbour, values)

    # =======================
    # Environmental sensing methods
    # =======================
    def measurement_update(self, color: Color) -> None:
        """
        Update the sensor's measurement of the environment.

        This method is called when the environment changes and triggers the
        measurement change callback if registered.

        Args:
            color (Color): New color measurement from the environment
        """
        if self._current_patch_color == color:
            return

        if self._on_measurement_change is not None:
            self._on_measurement_change(self, color)

        self._current_patch_color = deepcopy(color)

    def sensor_reading(self) -> Color:
        """
        Get the current sensor reading from the environment.

        Returns:
            Color: Current color of the grid patch the sensor is positioned on,
                or Color(-1, -1, -1) if no sensor manager is available
        """
        if self._sensor_manager is not None:
            return self._sensor_manager._grid.get_color(self.position)
        return Color(-1, -1, -1)

    # =======================
    # String representation and comparison
    # =======================
    def __repr__(self) -> str:
        """
        Return a string representation of the sensor.

        Returns:
            str: String representation including ID, coordinates, and color
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        Return a string representation of the sensor.

        Returns:
            str: Formatted string with sensor details
        """
        return f"Sensor: \n\tid = {self._id}\n\tcords = {self._cords}\n\tcolor = {self.color}"

    def __eq__(self, other: Sensor[T]) -> bool:
        """
        Check equality with another sensor based on ID.

        Args:
            other (Sensor[T]): The other sensor to compare with

        Returns:
            bool: True if sensors have the same ID, False otherwise
        """
        if not isinstance(other, Sensor):
            return False
        return self._id == other._id

    def __hash__(self) -> int:
        """
        Return hash of the sensor based on its ID.

        Returns:
            int: Hash value based on the sensor's unique ID
        """
        return hash(self.id)

    # =======================
    # Internal methods - DO NOT USE directly
    # =======================
    def _write_to_transmit_buffer(self, value: list[float]) -> None:
        """
        Write incoming messages to the transmission buffer.

        This is an internal method used by the communication system.

        Args:
            value (list[float]): Values to add to the pending message queue
        """
        self._pending_message_queue += value

    def _receive(self) -> None:
        """
        Process received messages by calling the receive callback.

        This is an internal method called by the sensor manager during updates.
        """
        msgs = deepcopy(self._message_queue)
        if len(msgs) == 0:
            return

        self._message_queue = []
        if self._on_receive is not None:
            self._on_receive(self, msgs)

    def _flush_run(self):
        """
        Flush the pending message queue to the active message queue.

        This is an internal method used by the simulation framework.
        """
        self._message_queue = deepcopy(self._pending_message_queue)
        self._pending_message_queue = []

    def _draw(self, surface: pygame.Surface, offset: PatchesGrid) -> None:
        """
        Draw the sensor on the pygame surface.

        This is an internal method used by the rendering system.

        Args:
            surface (pygame.Surface): The surface to draw on
            offset (PatchesGrid): Grid system for coordinate conversion
        """
        dot_radius = 5
        dot_color = self._current_color

        true_pos = offset.grid_to_pixel(int(self._cords.x), int(self._cords.y))
        pygame.draw.circle(surface, dot_color.to_tuple(), true_pos, dot_radius)


# =======================
# Utility functions for sensor creation
# =======================
def create_sensors(
    amount: int,
    grid: PatchesGrid,
    initial_state: Any = None,
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
    width = grid._grid_size - 1
    height = width

    coordinates = set()
    for _ in range(amount):
        current_cord = ()
        while current_cord in coordinates or current_cord == ():
            x = random.randint(0, width)
            y = random.randint(0, height)
            current_cord = (x, y)

        coordinates.add(current_cord)

    return [
        Sensor(
            cords=Coordinates(cord[0], cord[1]),
            patches=grid,
            initial_state=initial_state,
            on_receive=on_receive,
            on_measurement_change=on_measurement_change,
        )
        for cord in coordinates
    ]
