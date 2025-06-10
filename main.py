import sys

from src.components.sensor_manager import SensorManager
from src.components.sensors.default_sensor import DefaultSensor, create_default_sensors
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


def example(manager: SensorManager, grid: PatchesGrid) -> None:
    sensors = create_default_sensors(30, grid, {"state": "IDLE"}, on_read, on_write)
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_chain(sensors[:10])
    manager.connect_sensors_star(sensors[9], sensors[10:])
    sensors[0].write([1.0])


def main():
    engine = GeoNetEngine()
    engine.main_loop(example)
    sys.exit()


if __name__ == "__main__":
    main()
