from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Color:
    """
    A dataclass representing RGB color values with predefined color constants.

    This class provides color representation for the GeoNet application with
    validation and conversion utilities. It includes common color constants
    used throughout the application.

    Attributes:
        r (int): Red component (0-255)
        g (int): Green component (0-255)
        b (int): Blue component (0-255)

    Class Variables:
        Various predefined color constants like BLACK, WHITE, RED, etc.
    """

    r: int
    g: int
    b: int

    BLACK: ClassVar[Color]
    WHITE: ClassVar[Color]
    GRAY: ClassVar[Color]
    CONNECTION_GRAY: ClassVar[Color]
    LIGHT_GRAY: ClassVar[Color]
    GREEN: ClassVar[Color]
    RED: ClassVar[Color]
    BLUE: ClassVar[Color]
    CYAN: ClassVar[Color]
    CREAM: ClassVar[Color]
    SAGE: ClassVar[Color]
    LAVENDER: ClassVar[Color]
    SAND: ClassVar[Color]
    MINT: ClassVar[Color]
    DUSTY_ROSE: ClassVar[Color]
    NAVY: ClassVar[Color]
    FOREST: ClassVar[Color]

    def __post_init__(self) -> None:
        """
        Validate RGB values after initialization.

        Ensures all RGB values are within the valid range of 0-255.

        Raises:
            ValueError: If any RGB value is outside the range 0-255
        """
        if self.r > 255 or self.g > 255 or self.b > 255:
            raise ValueError(
                f"r, g, b must be below 255: r:{self.r}, g:{self.g}, b:{self.b}"
            )
        if self.r < 0 or self.g < 0 or self.b < 0:
            raise ValueError(
                f"r, g, b must be above 0: r:{self.r}, g:{self.g}, b:{self.b}"
            )

    def to_tuple(self) -> tuple[int, int, int]:
        """
        Convert the color to a tuple format suitable for pygame operations.

        Returns:
            tuple[int, int, int]: A tuple containing (r, g, b) values
        """
        return (self.r, self.g, self.b)


# Color constant definitions
Color.BLACK = Color(20, 20, 30)
Color.WHITE = Color(255, 255, 255)
Color.GRAY = Color(128, 128, 128)
Color.CONNECTION_GRAY = Color(90, 90, 90)
Color.LIGHT_GRAY = Color(64, 64, 64)

Color.GREEN = Color(0, 255, 0)
Color.RED = Color(255, 100, 100)
Color.BLUE = Color(100, 100, 255)
Color.CYAN = Color(0, 255, 255)

Color.CREAM = Color(245, 245, 220)
Color.SAGE = Color(188, 184, 138)
Color.LAVENDER = Color(230, 230, 250)
Color.SAND = Color(194, 178, 128)
Color.MINT = Color(152, 255, 152)
Color.DUSTY_ROSE = Color(220, 180, 180)
Color.NAVY = Color(0, 0, 128)
Color.FOREST = Color(34, 139, 34)
