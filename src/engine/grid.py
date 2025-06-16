"""
Grid system for spatial representation in the GeoNet simulation.

This module provides the PatchesGrid class that handles the spatial grid system,
coordinate transformations, and visual rendering of the simulation space.
"""

from __future__ import annotations

from typing import final

import pygame

from src.components.coords.coordinates import Coordinates

from .geo_color import Color


@final
class PatchesGrid:
    """
    A grid system for managing colored patches in a sensor network simulation.

    This class provides a grid-based coordinate system where each cell can have
    a specific color. It handles coordinate transformations between grid positions
    and pixel positions, and provides methods for setting colors of individual
    cells or rectangular regions.

    Attributes:
        _grid_size (int): Number of cells per side in the square grid
        _grid_width (int): Width of the grid in pixels
        _grid_height (int): Height of the grid in pixels
        _cell_size (float): Size of each cell in pixels
        _offset_x (int): Horizontal offset for centering the grid
        _offset_y (int): Vertical offset for centering the grid
        _cell_colors (dict[Coordinates, Color]): Mapping of grid positions to colors
    """

    # =======================
    # Initialization
    # =======================
    def __init__(
        self,
        screen_width: int,
        screen_height: int,
        grid_margin: int,
        grid_size: int,
    ) -> None:
        """
        Initialize the patches grid with specified dimensions and settings.

        Args:
            screen_width (int): Width of the screen in pixels
            screen_height (int): Height of the screen in pixels
            grid_margin (int): Margin around the grid in pixels
            grid_size (int): Number of cells per side in the square grid
        """
        self._grid_size = grid_size

        self._grid_width: int = min(
            screen_width - 2 * grid_margin, screen_height - 2 * grid_margin
        )
        self._grid_height: int = self._grid_width
        self._cell_size: float = self._grid_width / grid_size

        self._offset_x: int = (screen_width - self._grid_width) // 2 + 80
        self._offset_y: int = (screen_height - self._grid_height) // 2
        self._cell_colors: dict[Coordinates, Color] = {}
        self.fill_grid(Color.BLACK)

    # =======================
    # Cell information retrieval
    # =======================
    def get_color(self, cord: Coordinates) -> Color:
        """
        Get the color of a specific grid cell.

        Args:
            cord (Coordinates): The grid coordinates to query

        Returns:
            Color: The color of the specified cell

        Raises:
            ValueError: If coordinates are invalid or out of bounds
        """
        self._verify_cords(cord)
        return self._cell_colors[cord]

    # =======================
    # Cell modification and settings
    # =======================
    def set_color(self, cords: Coordinates, color: Color) -> None:
        """
        Set the color of a specific grid cell.

        Args:
            cords (Coordinates): The grid coordinates to modify
            color (Color): The color to set for the cell

        Raises:
            ValueError: If coordinates are invalid or out of bounds
        """
        self._verify_cords(cords)
        self._cell_colors[cords] = color

    def set_color_rect(
        self, starting_point: Coordinates, width: int, height: int, color: Color
    ) -> None:
        """
        Set the color of a rectangular region of grid cells.

        Args:
            starting_point (Coordinates): Top-left corner of the rectangle
            width (int): Width of the rectangle in cells
            height (int): Height of the rectangle in cells
            color (Color): The color to set for all cells in the rectangle

        Raises:
            ValueError: If any coordinates in the rectangle are invalid or out of bounds
        """
        for w in range(width):
            for h in range(height):
                current_cord = Coordinates(
                    x=starting_point.x + w,
                    y=starting_point.y + h,
                )
                self._verify_cords(current_cord)
                self.set_color(current_cord, color)

    def fill_grid(self, color: Color) -> None:
        """
        Fill the entire grid with a single color.

        Args:
            color (Color): The color to fill the entire grid with
        """
        self.set_color_rect(
            starting_point=Coordinates(0, 0),
            width=self._grid_size,
            height=self._grid_size,
            color=color,
        )

    def clear_color(self) -> None:
        """
        Clear the grid by filling it with black color.
        """
        self.fill_grid(Color.BLACK)

    # =======================
    # Coordinate conversion and positioning
    # =======================
    def grid_to_pixel(self, grid_x: int, grid_y: int) -> tuple[float, float]:
        """
        Convert grid coordinates to pixel coordinates (center of cell).

        Args:
            grid_x (int): X coordinate in the grid
            grid_y (int): Y coordinate in the grid

        Returns:
            tuple[float, float]: Pixel coordinates (x, y) at the center of the cell

        Raises:
            ValueError: If grid coordinates are invalid or out of bounds
        """
        self._verify_cords(Coordinates(grid_x, grid_y))
        pixel_x = int(self._offset_x + (grid_x + 0.5) * self._cell_size)
        pixel_y = int(self._offset_y + (grid_y + 0.5) * self._cell_size)
        return pixel_x, pixel_y

    def pixel_to_grid(self, x: float, y: float) -> tuple[bool, Coordinates]:
        """
        Convert pixel coordinates to grid coordinates.

        Args:
            x (float): X coordinate in pixels
            y (float): Y coordinate in pixels

        Returns:
            tuple[bool, Coordinates]: A tuple containing:
                - bool: True if the pixel is within the grid bounds, False otherwise
                - Coordinates: The corresponding grid coordinates (0,0 if out of bounds)
        """
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
    # Internal methods - DO NOT USE directly
    # =======================
    def _verify_cords(self, cord: Coordinates) -> None:
        """
        Validate that coordinates are within the grid bounds.

        This is an internal method used to ensure coordinates are valid before
        performing operations on grid cells.

        Args:
            cord (Coordinates): The coordinates to validate

        Raises:
            ValueError: If coordinates are not a Coordinates instance or are out of bounds
        """
        if self._grid_size <= cord.x or cord.x < 0:
            raise ValueError(
                f"Please stay inside the width confines of inclusive 0 to exclusive {self._grid_size} your value was {cord.x}"
            )
        if self._grid_size <= cord.y or cord.y < 0:
            raise ValueError(
                f"Please stay inside the height confines of inclusive 0 to exclusive {self._grid_size} your value was {cord.y}"
            )

    def _draw(self, screen: pygame.Surface) -> None:
        """
        Draw the grid and all its colored cells to the screen.

        This internal method renders the entire grid including cell colors,
        grid lines, and a border around the grid.

        Args:
            screen (pygame.Surface): The pygame surface to draw on
        """
        # Fill cells with their colors
        for cords, color in self._cell_colors.items():
            rect = pygame.Rect(
                self._offset_x + cords.x * self._cell_size,
                self._offset_y + cords.y * self._cell_size,
                self._cell_size,
                self._cell_size,
            )
            _ = pygame.draw.rect(screen, color.to_tuple(), rect)
        # Draw vertical lines
        for i in range(self._grid_size + 1):
            x = self._offset_x + i * self._cell_size
            _ = pygame.draw.line(
                screen,
                Color.LIGHT_GRAY.to_tuple(),
                (x, self._offset_y),
                (x, self._offset_y + self._grid_height),
                1,
            )

        # Draw horizontal lines
        for i in range(self._grid_size + 1):
            y = self._offset_y + i * self._cell_size
            _ = pygame.draw.line(
                screen,
                Color.LIGHT_GRAY.to_tuple(),
                (self._offset_x, y),
                (self._offset_x + self._grid_width, y),
                1,
            )

        # Draw grid border
        _ = pygame.draw.rect(
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
