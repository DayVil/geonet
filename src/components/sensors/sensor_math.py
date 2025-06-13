from src.components.sensors.sensor import Sensor


def euclid_distance(sensor1: Sensor, sensor2: Sensor) -> float:
    pos1 = sensor1.position()
    pos2 = sensor2.position()
    return pos1.euclid_distance(pos2)
