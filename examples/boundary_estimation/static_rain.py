from enum import Enum, auto
from typing import Any

from examples.boundary_estimation.scenarios import load_random_scenario
from src.components.sensors.sensor import Sensor, create_sensors
from src.components.sensors.sensor_connection_utils import (
    gg_connection,
)
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


class State(Enum):
    INIT = auto()
    IDLE = auto()
    BNDY = auto()
    OBNDY = auto()
    INSIDE = auto()
    OUTSIDE = auto()


def on_receive(sensor: Sensor, values: list[float]) -> None:
    current_state, send, patches = sensor.state

    if send:
        return

    if current_state == State.INIT:
        sensor.state = (State.IDLE, False, patches)
        sensor.broadcast(values)
        return

    color: Color = patches.get_color(sensor.position)
    if color == Color.NAVY:
        if all(value == 1.0 for value in values):
            sensor.state = (State.INSIDE, True, patches)
            sensor.color = Color.CYAN
        else:
            sensor.state = (State.BNDY, True, patches)
            sensor.color = Color.FOREST
    else:
        if all(value == 0.0 for value in values):
            sensor.state = (State.OUTSIDE, True, patches)
            sensor.color = Color.CREAM
        else:
            sensor.state = (State.OBNDY, True, patches)
            sensor.color = Color.RED


def setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    load_random_scenario(patches)
    sensors = create_sensors(
        amount=150,
        grid=patches,
        initial_state=(State.INIT, False, patches),
        on_receive=on_receive,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    for sensor in sensors:
        sensor.color = Color.SAGE


def on_update(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = manager.list_sensors()
    for sensor in sensors:
        if sensor.state[0] != State.INIT:
            continue
        color = patches.get_color(sensor.position)
        value = 1.0 if color == Color.NAVY else 0.0

        sensor.transmit(sensor, [value])


def static_rain_run():
    engine = GeoNetEngine()
    engine.main_loop(setup, update_fn=on_update)
