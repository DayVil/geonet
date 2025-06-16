from src.components.sensors.sensor import Sensor
from src.components.sensors.sensor_connection_utils import gg_connection
from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
from src.engine.grid import PatchesGrid


def on_receive(sensor: Sensor[bool], values: list[float]) -> None:
    if sensor.state:
        return

    sensor.state = True
    sensor.color = Color.GREEN
    sensor.broadcast(values)


def setup(manager: SensorManager, _patches: PatchesGrid) -> None:
    sensors = manager.create_and_append_sensors(
        amount=50, initial_state=False, on_receive=on_receive
    )
    manager.connect_sensors_if(sensors, gg_connection(sensors))
    sensors[0].transmit(sensors[0], [1.0])


def main():
    engine = GeoNetEngine(GeoNetConfig(window_title="GG Connection"))
    engine.main_loop(setup_fn=setup)


if __name__ == "__main__":
    main()
