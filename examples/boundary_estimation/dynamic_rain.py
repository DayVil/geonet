from enum import Enum, auto
import random
from typing import Any

from examples.boundary_estimation.scenarios import load_random_scenario
from src.components.sensors.sensor import Message, Sensor, create_sensors
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


def color_to_float(color: Color) -> float:
    if color == Color.NAVY:
        return 1.0
    else:
        return 0.0


def on_transmit(sensor: Sensor, msgs: list[Message]) -> None:
    send = sensor.state["send"]
    if len(msgs) > 0 and send:
        sensor.write_to_transmit_buffer(msgs)
        sensor.state["send"] = False


def on_receive(sensor: Sensor, msgs: list[Message]) -> list[Message]:
    state: State = sensor.state["current_state"]
    match state:
        case State.INIT:
            pass
        case State.IDLE:
            pass
        case State.BNDY:
            pass
    return msgs


def on_update(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    if global_state["count"] % 7 == 0:
        patches.clear_color()
        load_random_scenario(patches)

    global_state["count"] += 1

    sensors = manager.list_sensors()
    for sensor in sensors:
        state = sensor.state["current_state"]
        if random.random() > 0.9 and state == State.INIT:
            patch_color = color_to_float(patches.get_color(sensor.position))
            sensor.transmit(sensor.id, [patch_color])
    return global_state


def on_change(sensor: Sensor, color: Color) -> None:
    pass


def setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=90,
        grid=patches,
        initial_state={"current_state": State.INIT, "send": True},
        on_receive=on_receive,
        on_transmit=on_transmit,
        on_measurement_change=on_change,
    )
    for sensor in sensors:
        sensor.color = Color.CREAM
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    global_state = {"count": 0}
    return global_state


def dynamic_rain_run():
    engine = GeoNetEngine()
    engine.main_loop(setup_fn=setup, update_fn=on_update)
