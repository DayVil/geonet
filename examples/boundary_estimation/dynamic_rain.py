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


def on_transmit(sensor: Sensor, msgs: list[Message]) -> None:
    pass


def on_receive(sensor: Sensor, msgs: list[Message]) -> list[Message]:
    return msgs


def on_update(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    if global_state["count"] % 7 == 0:
        patches.clear_color()
        load_random_scenario(patches)

    global_state["count"] += 1
    return global_state


def setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=90,
        grid=patches,
        initial_state={"current_state": State.IDLE, "send": False},
        on_receive=on_receive,
        on_transmit=on_transmit,
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
