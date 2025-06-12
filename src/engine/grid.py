from __future__ import annotations

import pygame

from src.components.sensors.sensor import Cords

from .geo_color import Colors


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
        self._cell_colors: dict[Cords, Colors] = {}

    # =======================
    # Settings of Cells
    # =======================
    def set_color(self, cords: Cords, color: Colors) -> None:
        self._verify_cords(cords)
        self._cell_colors[cords] = color

    def set_color_rect(
        self, starting_point: Cords, width: int, height: int, color: Colors
    ) -> None:
        for w in range(width):
            for h in range(height):
                current_cord = Cords(
                    x=starting_point.x + w,
                    y=starting_point.y + h,
                )
                self._verify_cords(current_cord)
                self.set_color(current_cord, color)

    def fill_grid(self, color: Colors) -> None:
        self.set_color_rect(
            starting_point=Cords(0, 0),
            width=self._grid_size,
            height=self._grid_size,
            color=color,
        )

    # =======================
    # Positioning of Components
    # =======================
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[float, float]:
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        self._verify_cords(Cords(grid_x, grid_y))
        pixel_x = int(self._offset_x + (grid_x + 0.5) * self._cell_size)
        pixel_y = int(self._offset_y + (grid_y + 0.5) * self._cell_size)
        return pixel_x, pixel_y

    # =======================
    # DO NOT USE
    # =======================
    def _verify_cords(self, cord: Cords) -> None:
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
                Colors.LIGHT_GRAY.to_tuple(),
                (x, self._offset_y),
                (x, self._offset_y + self._grid_height),
                1,
            )

        # Draw horizontal lines
        for i in range(self._grid_size + 1):
            y = self._offset_y + i * self._cell_size
            pygame.draw.line(
                screen,
                Colors.LIGHT_GRAY.to_tuple(),
                (self._offset_x, y),
                (self._offset_x + self._grid_width, y),
                1,
            )

        # Draw grid border
        pygame.draw.rect(
            screen,
            Colors.GRAY.to_tuple(),
            (
                self._offset_x,
                self._offset_y,
                self._grid_width,
                self._grid_height,
            ),
            2,
        )
