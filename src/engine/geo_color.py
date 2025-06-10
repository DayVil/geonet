from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Colors:
    r: int
    g: int
    b: int

    BLACK: ClassVar[Colors]
    WHITE: ClassVar[Colors]
    GRAY: ClassVar[Colors]
    CONNECTION_GRAY: ClassVar[Colors]
    LIGHT_GRAY: ClassVar[Colors]
    GREEN: ClassVar[Colors]
    RED: ClassVar[Colors]
    BLUE: ClassVar[Colors]
    CYAN: ClassVar[Colors]

    def __post_init__(self) -> None:
        if self.r > 255 or self.g > 255 or self.b > 255:
            raise ValueError(
                f"r, g, b must be below 255: r:{self.r}, g:{self.g}, b:{self.b}"
            )
        if self.r < 0 or self.g < 0 or self.b < 0:
            raise ValueError(
                f"r, g, b must be above 0: r:{self.r}, g:{self.g}, b:{self.b}"
            )

    def to_tuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)


Colors.BLACK = Colors(20, 20, 30)
Colors.WHITE = Colors(255, 255, 255)
Colors.GRAY = Colors(128, 128, 128)
Colors.CONNECTION_GRAY = Colors(90, 90, 90)
Colors.LIGHT_GRAY = Colors(64, 64, 64)

Colors.GREEN = Colors(0, 255, 0)
Colors.RED = Colors(255, 100, 100)
Colors.BLUE = Colors(100, 100, 255)
Colors.CYAN = Colors(0, 255, 255)
