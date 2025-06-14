from enum import Enum, auto


class State(Enum):
    IDLE = auto()
    BNDY = auto()
    OBNDY = auto()
    INSIDE = auto()
    OUTSIDE = auto()
