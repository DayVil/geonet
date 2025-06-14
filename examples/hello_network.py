from typing import Any

from src.components.sensors.sensor import Message, Sensor, create_sensors
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor, msgs: list[Message]) -> list[Message]:
    if len(msgs) == 0:
        sensor.color = Color.CYAN
        return []
    else:
        sensor.color = Color.GREEN
        return msgs


def on_transmit(sensor: Sensor, msgs: list[Message]) -> None:
    if sensor.state["state"] == "IDLE":
        sensor.write_to_transmit_buffer(msgs)
        sensor.state["state"] = "SEND"


def scenario(manager: SensorManager, patches: PatchesGrid, global_state: Any) -> Any:
    sensors = create_sensors(
        amount=20,
        grid=patches,
        initial_state={"state": "IDLE"},
        on_receive=on_receive,
        on_transmit=on_transmit,
    )
    manager.append_multiple_sensors(sensors)
    manager.connect_sensors_chain(sensors)
    manager.connect_sensors_star(sensors[10], sensors[11:15])

    sensors[0].transmit(sensors[0].id, [0])


def main():
    engine = GeoNetEngine()
    engine.main_loop(setup_fn=scenario)


if __name__ == "__main__":
    main()
