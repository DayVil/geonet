"""
Main GeoNet simulation engine and configuration.

This module contains the core GeoNet simulation engine that handles pygame display,
event processing, and coordinates the simulation loop between sensors and the grid system.
"""

from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass
from typing import Any

import pygame

from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


@dataclass(frozen=True)
class GeoNetConfig:
    """
    Configuration settings for the GeoNet simulation engine.

    This dataclass contains all the configurable parameters for the GeoNet
    simulation including display settings, grid parameters, and timing settings.

    Attributes:
        screen_width (int): Width of the application window in pixels. Defaults to 1000.
        screen_heigth (int): Height of the application window in pixels. Defaults to 800.
        window_title (str): Title displayed in the window title bar. Defaults to "GeoNet".
        grid_size (int): Number of cells in the grid (square grid). Defaults to 55.
        grid_margin (int): Margin around the grid in pixels. Defaults to 10.
        fps (int): Target frames per second for the display. Defaults to 60.
        update_interval (int): Milliseconds between simulation updates. Defaults to 700.
    """

    screen_width: int = 1000
    screen_heigth: int = 800
    window_title: str = "GeoNet"

    grid_size: int = 55
    grid_margin: int = 10

    fps: int = 60
    update_interval: int = 700


class GeoNetEngine:
    """
    The main engine class for the GeoNet sensor network simulation.

    This class manages the pygame display, handles events, updates the simulation,
    and coordinates between the grid system and sensor manager. It provides the
    main simulation loop and user interaction handling.

    Attributes:
        _cfg (GeoNetConfig): Configuration settings for the engine
        _quit (bool): Flag indicating if the simulation should terminate
        _clock (pygame.time.Clock): Pygame clock for controlling frame rate
        _screen (pygame.Surface): Main display surface
        _grid (PatchesGrid): The grid system for the simulation
        _sensor_manager (SensorManager): Manager for all sensors in the simulation
        _tick_counter (int): Counter for simulation ticks
        _font (pygame.font.Font): Font for rendering text
    """

    def __init__(self, config: GeoNetConfig | None = None) -> None:
        """
        Initialize the GeoNet engine with the given configuration.

        Args:
            config (GeoNetConfig | None): Configuration object. If None, default config is used.
        """
        if config is None:
            cfg = GeoNetConfig()
        else:
            cfg = deepcopy(config)

        self._cfg = cfg
        self._quit = False
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(
            (self._cfg.screen_width, self._cfg.screen_heigth), pygame.DOUBLEBUF
        )
        pygame.display.set_caption(self._cfg.window_title)

        self._grid = PatchesGrid(
            screen_width=self._cfg.screen_width,
            screen_height=self._cfg.screen_heigth,
            grid_size=self._cfg.grid_size,
            grid_margin=self._cfg.grid_margin,
        )
        self._sensor_manager = SensorManager(self._grid)

        self._tick_counter = 0
        pygame.font.init()
        self._font = pygame.font.Font(None, 24)

    def _handle_events(self) -> None:
        """
        Process pygame events including window close, keyboard input, and mouse clicks.

        Handles:
        - Window close button and ESC key for quitting
        - Mouse clicks for sensor inspection (prints sensor info to console)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    is_valid, grid_pos = self._grid.pixel_to_grid(mouse_x, mouse_y)
                    if is_valid:
                        print("=" * 10)
                        print(f"Clicked grid position: {grid_pos}")
                        sensors = self._sensor_manager.list_sensors()
                        for sensor in sensors:
                            if sensor.position == grid_pos:
                                print(sensor)
                                break
                        print("=" * 10)
                        print()

    def _update(
        self,
        update_fn: Callable[[SensorManager, PatchesGrid, Any], Any] | None,
        global_state: Any,
    ) -> Any:
        """
        Update the simulation state by calling the user-provided update function.

        Args:
            update_fn (Callable | None): User-defined update function that receives
                the sensor manager, grid, and global state
            global_state (Any): Current global state of the simulation

        Returns:
            Any: Updated global state returned from the update function
        """

        def inner_update(global_state: Any) -> Any:
            if update_fn is not None:
                return update_fn(self._sensor_manager, self._grid, global_state)
            return global_state

        new_global_state = self._sensor_manager._update(inner_update, global_state)
        return new_global_state

    def _draw(self) -> None:
        """
        Render the current simulation state to the screen.

        Draws the grid, sensors, connections, and displays the tick counter.
        """
        self._tick_counter += 1

        self._screen.fill(Color.BLACK.to_tuple())

        tick_text = self._font.render(
            f"Ticks: {self._tick_counter}", True, Color.WHITE.to_tuple()
        )
        tick_x = 10
        tick_y = 10
        self._screen.blit(tick_text, (tick_x, tick_y))

        self._grid._draw(self._screen)
        self._sensor_manager._draw(self._screen)
        pygame.display.flip()

    def main_loop(
        self,
        setup_fn: Callable[[SensorManager, PatchesGrid, Any], Any] | None = None,
        update_fn: Callable[[SensorManager, PatchesGrid, Any], Any] | None = None,
    ) -> None:
        """
        Run the main simulation loop.

        This method initializes the simulation with the setup function and then
        continuously runs the simulation loop, processing events, updating state,
        and rendering the display at the configured intervals.

        Args:
            setup_fn (Callable | None): Optional function called once at startup
                to initialize the simulation. Receives sensor manager, grid, and
                initial global state (None).
            update_fn (Callable | None): Optional function called every update
                interval to update the simulation state. Receives sensor manager,
                grid, and current global state.
        """
        global_state: Any = None
        if setup_fn is not None:
            new_state = setup_fn(self._sensor_manager, self._grid, global_state)
            global_state = deepcopy(new_state)
        last_draw_time = pygame.time.get_ticks()
        first_draw = True
        while not self._quit:
            self._handle_events()

            current_time = pygame.time.get_ticks()
            if current_time - last_draw_time >= self._cfg.update_interval or first_draw:
                new_global_state = self._update(update_fn, global_state)
                self._draw()
                first_draw = False
                global_state = deepcopy(new_global_state)
                last_draw_time = pygame.time.get_ticks()

            self._clock.tick(self._cfg.fps)

        pygame.quit()
