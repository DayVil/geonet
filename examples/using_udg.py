from typing import Any

from src.components.sensors.sensor import Sensor, create_sensors
from src.components.sensors.sensor_connection_utils import (
    udg_connection,
    udg_connection_autotune,
)
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor, values: list[float]) -> None:
    if sensor.state:
        return

    sensor.state = True
    sensor.color = Color.GREEN
    sensor.broadcast(values)


def udg_autotune_setup(
    manager: SensorManager, patches: PatchesGrid, global_state: Any
) -> Any:
    sensors = create_sensors(
        amount=50, grid=patches, initial_state=False, on_receive=on_receive
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, udg_connection_autotune(manager, sensors))
    sensors[0].transmit(sensors[0], [1.0])


def udg_setup(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=50, grid=patches, initial_state=False, on_receive=on_receive
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_if(sensors, udg_connection(10))
    sensors[0].transmit(sensors[0], [1.0])


def main():
    udg_engine = GeoNetEngine(GeoNetConfig(window_title="UDG"))
    udg_engine.main_loop(setup_fn=udg_setup)

    udg_autotune_engine = GeoNetEngine(GeoNetConfig(window_title="Autotune UDG"))
    udg_autotune_engine.main_loop(setup_fn=udg_autotune_setup)


if __name__ == "__main__":
    main()
