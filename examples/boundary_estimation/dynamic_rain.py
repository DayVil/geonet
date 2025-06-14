from enum import Enum, auto
from typing import Any

from examples.boundary_estimation.scenarios import load_random_scenario
from src.components.sensors.sensor import Sensor, create_sensors
from src.components.sensors.sensor_connection_utils import (
    gg_connection,
)
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
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


def on_receive(sensor: Sensor, values: list[float]) -> None:
    # send = sensor.state["send"]
    if len(values) == 0:
        return

    state: State = sensor.state["current_state"]

    match state:
        case State.INIT:
            patch_color = sensor.sensor_reading()
            color_value = color_to_float(patch_color)
            sensor.state["current_state"] = State.IDLE
            sensor.broadcast([color_value])

        case State.IDLE:
            curr_color_val = color_to_float(sensor.sensor_reading())
            if curr_color_val == 1.0:
                if all(val == 1.0 for val in values):
                    sensor.color = Color.CYAN
                else:
                    sensor.color = Color.FOREST
            else:
                if all(val == 0.0 for val in values):
                    sensor.color = Color.CREAM
                else:
                    sensor.color = Color.RED

            sensor.state["current_state"] = State.BNDY

        case State.BNDY:
            pass


def on_update(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    if global_state["count"] % 7 == 0:
        patches.clear_color()
        load_random_scenario(patches)

    sensors = manager.list_sensors()
    if global_state["count"] % 4 == 0:
        for sensor in sensors:
            sensor.state["current_state"] = State.INIT

    global_state["count"] += 1

    for sensor in sensors:
        state = sensor.state["current_state"]
        if state == State.INIT:
            patch_color = color_to_float(sensor.sensor_reading())
            sensor.transmit(to_sensor=sensor, values=[patch_color])

    return global_state


def setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=90,
        grid=patches,
        initial_state={"current_state": State.INIT, "send": False},
        on_receive=on_receive,
    )
    for sensor in sensors:
        sensor.color = Color.CREAM
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    global_state = {"count": 0}
    return global_state


def dynamic_rain_run():
    engine = GeoNetEngine(GeoNetConfig(window_title="Dynamic Rain"))
    engine.main_loop(setup_fn=setup, update_fn=on_update)
