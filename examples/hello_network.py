from src.components.sensor_manager import SensorManager
from src.components.sensors.default_sensor import DefaultSensor, create_default_sensors
from src.engine.geo_color import Colors
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: DefaultSensor, value: list[float]) -> list[float]:
    if len(value) == 0:
        sensor.color = Colors.CYAN
        return []
    else:
        sensor.color = Colors.GREEN
        return value


def on_transmit(sensor: DefaultSensor, value: list[float]) -> None:
    if sensor.state["state"] == "IDLE":
        sensor.write_to_mem(value)
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

    sensors[0].transmit([1])


def main():
    engine = GeoNetEngine()
    engine.main_loop(scenario)


if __name__ == "__main__":
    main()
