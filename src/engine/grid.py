from __future__ import annotations

import pygame

from .geo_color import Colors


class Grid:
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

    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[float, float]:
        """Convert grid coordinates to pixel coordinates (center of cell)"""
        pixel_x = self._offset_x + (grid_x + 0.5) * self._cell_size
        pixel_y = self._offset_y + (grid_y + 0.5) * self._cell_size
        return pixel_x, pixel_y

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the grid lines"""
        # Draw vertical lines
        for i in range(self._grid_size + 1):
            x = self._offset_x + i * self._cell_size
            pygame.draw.line(
                screen,
                Colors.LIGHT_GRAY,
                (x, self._offset_y),
                (x, self._offset_y + self._grid_height),
                1,
            )

        # Draw horizontal lines
        for i in range(self._grid_size + 1):
            y = self._offset_y + i * self._cell_size
            pygame.draw.line(
                screen,
                Colors.LIGHT_GRAY,
                (self._offset_x, y),
                (self._offset_x + self._grid_width, y),
                1,
            )

        # Draw grid border
        pygame.draw.rect(
            screen,
            Colors.GRAY,
            (
                self._offset_x,
                self._offset_y,
                self._grid_width,
                self._grid_height,
            ),
            2,
        )
