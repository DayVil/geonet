from src.components.sensors.sensor import Sensor, create_default_sensors
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor, value: list[float]) -> list[float]:
    if len(value) == 0:
        sensor.color = Color.CYAN
        return []
    else:
        sensor.color = Color.GREEN
        return value


def on_transmit(sensor: Sensor, value: list[float]) -> None:
    if sensor.state["state"] == "IDLE":
        sensor.write_to_transmit_buffer(value)
        sensor.state["state"] = "SEND"


def scenario(manager: SensorManager, patches: PatchesGrid) -> None:
    sensors = create_default_sensors(
        amount=20,
        grid=patches,
        initial_state={"state": "IDLE"},
        on_receive=on_receive,
        on_transmit=on_transmit,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_chain(sensors)
    manager.connect_sensors_star(sensors[10], sensors[11:15])

    sensors[0].transmit([1.0])


def main():
    engine = GeoNetEngine()
    engine.main_loop(scenario)


if __name__ == "__main__":
    main()
