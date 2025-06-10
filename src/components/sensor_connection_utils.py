from collections.abc import Callable, Sequence

from src.components.sensor_math import euclid_distance
from src.components.sensors.sensor import Sensor


def udg_connection(
    distance: int,
) -> Callable[[Sensor, Sensor, Sequence[Sensor] | None], bool]:
    internal_distance = distance

    def udg_connection_stub(
        sensor1: Sensor, sensor2: Sensor, _: Sequence[Sensor] | None = None
    ) -> bool:
        if euclid_distance(sensor1, sensor2) < internal_distance:
            return True
        return False

    return udg_connection_stub
