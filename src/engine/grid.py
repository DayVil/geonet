from __future__ import annotations

import pygame

from src.components.sensors.sensor import Coordinates

from .geo_color import Color


class PatchesGrid:
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        grid_margin: int,
        grid_size: int,
    ) -> None:
        self._grid_size = grid_size

        self._grid_width: int = min(
            screen_width - 2 * grid_margin, screen_height - 2 * grid_margin
        )
        self._grid_height: int = self._grid_width
        self._cell_size: float = self._grid_width / grid_size

        self._offset_x: int = (screen_width - self._grid_width) // 2
        self._offset_y: int = (screen_height - self._grid_height) // 2
        self._cell_colors: dict[Coordinates, Color] = {}
        self.fill_grid(Color.BLACK)

    # =======================
    # Fetch cell information
    # =======================
    def get_color(self, cord: Coordinates) -> Color:
        self._verify_cords(cord)
        return self._cell_colors[cord]

    # =======================
    # Settings of Cells
    # =======================
    def set_color(self, cords: Coordinates, color: Color) -> None:
        self._verify_cords(cords)
        self._cell_colors[cords] = color

    def set_color_rect(
        self, starting_point: Coordinates, width: int, height: int, color: Color
    ) -> None:
        for w in range(width):
            for h in range(height):
                current_cord = Coordinates(
                    x=starting_point.x + w,
                    y=starting_point.y + h,
                )
                self._verify_cords(current_cord)
                self.set_color(current_cord, color)

    def fill_grid(self, color: Color) -> None:
        self.set_color_rect(
            starting_point=Coordinates(0, 0),
            width=self._grid_size,
            height=self._grid_size,
            color=color,
        )

    # =======================
    # Positioning of Components
    # =======================
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[float, float]:
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        self._verify_cords(Coordinates(grid_x, grid_y))
        pixel_x = int(self._offset_x + (grid_x + 0.5) * self._cell_size)
        pixel_y = int(self._offset_y + (grid_y + 0.5) * self._cell_size)
        return pixel_x, pixel_y

    def pixel_to_grid(self, x: float, y: float) -> tuple[bool, Coordinates]:
        """Convert pixel coordinates to grid coordinates."""
        if (
            x < self._offset_x
            or x >= self._offset_x + self._grid_width
            or y < self._offset_y
            or y >= self._offset_y + self._grid_height
        ):
            return False, Coordinates(0, 0)
        grid_x = int((x - self._offset_x) / self._cell_size)
        grid_y = int((y - self._offset_y) / self._cell_size)

        try:
            self._verify_cords(Coordinates(grid_x, grid_y))
            return True, Coordinates(grid_x, grid_y)
        except ValueError:
            return False, Coordinates(0, 0)

    # =======================
    # DO NOT USE
    # =======================
    def _verify_cords(self, cord: Coordinates) -> None:
        if not isinstance(cord, Coordinates):
            raise ValueError(
                f"cord may only be of type Coordinates but received: {type(cord)}"
            )
        if self._grid_size <= cord.x or cord.x < 0:
            raise ValueError(
                f"Please stay inside the width confines of inclusive 0 to exclusive {self._grid_size} your value was {cord.x}"
            )
        if self._grid_size <= cord.y or cord.y < 0:
            raise ValueError(
                f"Please stay inside the height confines of inclusive 0 to exclusive {self._grid_size} your value was {cord.y}"
            )

    def _draw(self, screen: pygame.Surface) -> None:
        """Draw the grid lines"""
        # Fill cells with their colors
        for cords, color in self._cell_colors.items():
            rect = pygame.Rect(
                self._offset_x + cords.x * self._cell_size,
                self._offset_y + cords.y * self._cell_size,
                self._cell_size,
                self._cell_size,
            )
            pygame.draw.rect(screen, color.to_tuple(), rect)
        # Draw vertical lines
        for i in range(self._grid_size + 1):
            x = self._offset_x + i * self._cell_size
            pygame.draw.line(
                screen,
                Color.LIGHT_GRAY.to_tuple(),
                (x, self._offset_y),
                (x, self._offset_y + self._grid_height),
                1,
            )

        # Draw horizontal lines
        for i in range(self._grid_size + 1):
            y = self._offset_y + i * self._cell_size
            pygame.draw.line(
                screen,
                Color.LIGHT_GRAY.to_tuple(),
                (self._offset_x, y),
                (self._offset_x + self._grid_width, y),
                1,
            )

        # Draw grid border
        pygame.draw.rect(
            screen,
            Color.GRAY.to_tuple(),
            (
                self._offset_x,
                self._offset_y,
                self._grid_width,
                self._grid_height,
            ),
            2,
        )
