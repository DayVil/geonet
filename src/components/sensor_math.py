import math

from src.components.sensors.sensor import Sensor


def euclid_distance(sensor1: Sensor, sensor2: Sensor) -> float:
    pos1 = sensor1.position()
    pos2 = sensor2.position()
    distance = math.sqrt((pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2)
    return distance
