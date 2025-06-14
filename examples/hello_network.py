from typing import Any

from src.components.sensors.sensor import Sensor, create_sensors
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor, values: list[float]) -> None:
    if sensor.state["state"] != "IDLE":
        return

    sensor.color = Color.GREEN
    sensor.state["state"] = "SEND"

    for neighbour in sensor.neighbours:
        sensor.transmit(neighbour, values)


def scenario(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=20,
        grid=patches,
        initial_state={"state": "IDLE"},
        on_receive=on_receive,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_chain(sensors)
    manager.connect_sensors_star(sensors[10], sensors[11:15])

    sensors[0].transmit(to_sensor=sensors[0], values=[0])


def main():
    engine = GeoNetEngine(GeoNetConfig(window_title="Hello Network"))
    engine.main_loop(setup_fn=scenario)


if __name__ == "__main__":
    main()
