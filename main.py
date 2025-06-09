import sys

from src.components.sensor_manager import SensorManager
from src.components.sensors.default_sensor import DefaultSensor
from src.components.sensors.sensor import Cords
from src.engine.geo_color import Colors
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


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


def example(manager: SensorManager, field: PatchesGrid) -> None:
    sensors = [
        DefaultSensor(
            cords=Cords(1, 1),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(3, 3),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(5, 7),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(0, 10),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(20, 20),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(7, 0),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(39, 39),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
    ]

    sensors2 = [
        DefaultSensor(
            cords=Cords(11, 23),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(21, 23),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
        DefaultSensor(
            cords=Cords(4, 4),
            initial_state={"state": "IDLE"},
            on_read=on_read,
            on_write=on_write,
        ),
    ]

    sensors = manager.append_multiple_sensors(sensors)
    sensors[0].write([1.0])

    manager.connect_sensors_chain(sensors)
    manager.connect_sensors_star(sensors[3], sensors2)


def main():
    engine = GeoNetEngine()
    engine.main_loop(example)
    sys.exit()


if __name__ == "__main__":
    main()
