import sys

from src.components.sensor_manager import SensorManager
from src.components.sensor_math import euclid_distance
from src.components.sensors.default_sensor import DefaultSensor
from src.components.sensors.sensor import Cords
from src.engine.geo_color import Colors
from src.engine.geonet import GeoNetEngine


def on_read(sensor: DefaultSensor, value: list[float]) -> list[float]:
    if len(value) == 0:
        sensor.set_color(Colors.CYAN)
        return []
    else:
        sensor.set_color(Colors.GREEN)
        return value


def on_write(sensor: DefaultSensor, value: list[float]) -> None:
    if sensor.state["state"] == "IDLE":
        sensor.write_to_mem(value)
        sensor.state["state"] = "SEND"


def example(manager: SensorManager) -> None:
    sensor1 = DefaultSensor(
        Cords(0, 0),
        initial_state={"state": "IDLE"},
        on_read=on_read,
        on_write=on_write,
    )
    sensor1.write([2])
    sensor2 = DefaultSensor(
        Cords(10, 20),
        initial_state={"state": "IDLE"},
        on_read=on_read,
        on_write=on_write,
    )
    sensor3 = DefaultSensor(
        Cords(20, 0),
        initial_state={"state": "IDLE"},
        on_read=on_read,
        on_write=on_write,
    )
    manager.append_sensor(sensor1)
    manager.append_sensor(sensor2)
    manager.append_sensor(sensor3)
    manager.connect_sensors(sensor1, sensor2, euclid_distance)
    manager.connect_sensors(sensor3, sensor2, euclid_distance)


def main():
    engine = GeoNetEngine()
    engine.main_loop(example)
    sys.exit()


if __name__ == "__main__":
    main()
