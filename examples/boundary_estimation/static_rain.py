from typing import Any

from examples.boundary_estimation.scenarios import load_random_scenario
from examples.boundary_estimation.state import State
from src.components.sensors.sensor import Message, Sensor, create_sensors
from src.components.sensors.sensor_connection_utils import (
    gg_connection,
)
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor, msgs: list[Message]) -> list[Message]:
    _, _, patches = sensor.state

    color: Color = patches.get_color(sensor.position)
    if color == Color.NAVY:
        if all(msg.value == 1.0 for msg in msgs):
            sensor.state = (State.INSIDE, True, patches)
            sensor.color = Color.CYAN
        else:
            sensor.state = (State.BNDY, True, patches)
            sensor.color = Color.FOREST
    else:
        if all(msg.value == 0.0 for msg in msgs):
            sensor.state = (State.OUTSIDE, True, patches)
            sensor.color = Color.CREAM
        else:
            sensor.state = (State.OBNDY, True, patches)
            sensor.color = Color.RED

    return []


def on_transmit(sensor: Sensor, msgs: list[Message]) -> None:
    _, send, _ = sensor.state
    if not send:
        sensor.write_to_transmit_buffer(msgs)


def setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    load_random_scenario(patches)
    sensors = create_sensors(
        amount=150,
        grid=patches,
        initial_state=(State.IDLE, False, patches),
        on_receive=on_receive,
        on_transmit=on_transmit,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    for sensor in sensors:
        sensor.color = Color.SAGE


def on_update(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = manager.list_sensors()
    for sensor in sensors:
        if sensor.state[0] != State.IDLE:
            continue
        color = patches.get_color(sensor.position)
        value = 1.0 if color == Color.NAVY else 0.0

        neigbours = sensor.neighbours
        for neighbour in neigbours:
            neighbour.transmit(sensor.id, [value])


def static_rain_run():
    engine = GeoNetEngine()
    engine.main_loop(setup, update_fn=on_update)
