from enum import Enum, auto

from src.components.coordinates import Coordinates
from src.components.sensors.sensor import Sensor, create_default_sensors
from src.components.sensors.sensor_connection_utils import gg_connection
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


class State(Enum):
    IDLE = auto()
    BNDY = auto()
    OBNDY = auto()
    INSIDE = auto()
    OUTSIDE = auto()


def on_receive(sensor: Sensor, value: list[float]) -> list[float]:
    _, _, patches = sensor.state

    color: Color = patches.get_color(sensor.position)
    if color == Color.NAVY:
        if all(val == 1.0 for val in value):
            sensor.state = (State.INSIDE, True, patches)
            sensor.color = Color.CYAN
        else:
            sensor.state = (State.BNDY, True, patches)
            sensor.color = Color.FOREST
    else:
        if all(val == 0.0 for val in value):
            sensor.state = (State.OUTSIDE, True, patches)
            sensor.color = Color.CREAM
        else:
            sensor.state = (State.OBNDY, True, patches)
            sensor.color = Color.RED

    return []


def on_transmit(sensor: Sensor, value: list[float]) -> None:
    _, send, _ = sensor.state
    if not send:
        sensor.write_to_transmit_buffer(value)


def setup(manager: SensorManager, patches: PatchesGrid) -> None:
    patches.set_color_rect(
        starting_point=Coordinates(12, 25),
        width=35,
        height=15,
        color=Color.NAVY,
    )
    patches.set_color_rect(
        starting_point=Coordinates(15, 22),
        width=25,
        height=20,
        color=Color.NAVY,
    )
    patches.set_color_rect(
        starting_point=Coordinates(20, 10),
        width=25,
        height=20,
        color=Color.NAVY,
    )
    sensors = create_default_sensors(
        amount=90,
        grid=patches,
        initial_state=(State.IDLE, False, patches),
        on_receive=on_receive,
        on_transmit=on_transmit,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, gg_connection(sensors))

    for sensor in sensors:
        sensor.color = Color.SAGE


def on_update(manager: SensorManager, patches: PatchesGrid) -> None:
    sensors = manager.list_sensors()
    for sensor in sensors:
        color = patches.get_color(sensor.position)
        value = 1.0 if color == Color.NAVY else 0.0

        neigbours = sensor.neighbours
        for neighbour in neigbours:
            neighbour.transmit([value])


def static_rain_run():
    engine = GeoNetEngine()
    engine.main_loop(setup, update_fn=on_update)
