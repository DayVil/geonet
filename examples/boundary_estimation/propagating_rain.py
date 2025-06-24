from enum import Enum, auto

from examples.boundary_estimation.scenarios import load_random_scenario
from src.components.sensors.sensor import Sensor
from src.components.sensors.sensor_connection_utils import (
    gg_connection,
)
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
from src.engine.grid import PatchesGrid


class State(Enum):
    # INIT = auto()
    REC = auto()
    FIN = auto()


StateContainer = dict[str, State | bool]
GlobalStateContainer = dict[str, int]


PING = [0.0]


def color_to_float(color: Color) -> float:
    return 1.0 if color == Color.NAVY else 0.0


def sensor_readings_to_float(sensors: list[Sensor[StateContainer]]) -> list[float]:
    readings: list[float] = []
    for sensor in sensors:
        value = color_to_float(sensor.sensor_reading())
        readings.append(value)
    return readings


def on_change(sensor: Sensor[StateContainer], _color: Color) -> None:
    state = sensor.state["current_state"]
    if state == State.REC:
        sensor.transmit(to_sensor=sensor, values=PING)
        sensor.broadcast(PING)


def on_receive(sensor: Sensor[StateContainer], values: list[float]) -> None:
    if len(values) == 0:
        return

    state = sensor.state["current_state"]

    match state:
        case State.REC:
            curr_color_val = color_to_float(sensor.sensor_reading())
            neigbour_readings = sensor_readings_to_float(sensor.neighbours)
            if curr_color_val == 1.0:
                if all(val == 1.0 for val in neigbour_readings):
                    sensor.color = Color.CYAN
                else:
                    sensor.color = Color.FOREST
            else:
                if all(val == 0.0 for val in neigbour_readings):
                    sensor.color = Color.CREAM
                else:
                    sensor.color = Color.RED

            sensor.state["current_state"] = State.FIN
            sensor.broadcast(PING)

        case _:
            pass


def on_update(
    manager: SensorManager, patches: PatchesGrid, global_state: GlobalStateContainer
) -> GlobalStateContainer:
    if global_state["count"] % 7 == 0:
        patches.clear_color()
        load_random_scenario(patches)
        sensors: list[Sensor[StateContainer]] = manager.list_sensors()
        for sensor in sensors:
            sensor.state["current_state"] = State.REC

    global_state["count"] += 1

    return global_state


def setup(manager: SensorManager, _patches: PatchesGrid) -> GlobalStateContainer:
    sensors = manager.create_and_append_sensors(
        amount=90,
        initial_state={"current_state": State.REC, "send": False},
        on_receive=on_receive,
        on_measurement_change=on_change,
    )
    for sensor in sensors:
        sensor.color = Color.CREAM
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    global_state = {"count": 0}
    return global_state


def propagating_rain_run():
    cfg = GeoNetConfig(window_title="Propagating Rain", update_interval=400)
    engine = GeoNetEngine(cfg)
    engine.main_loop(setup_fn=setup, update_fn=on_update)
