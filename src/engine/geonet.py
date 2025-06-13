from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass

import pygame

from src.components.sensors.sensor_manager import SensorManager
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


@dataclass(frozen=True)
class GeoNetConfig:
    screen_width: int = 1000
    screen_heigth: int = 800

    grid_size: int = 55
    grid_margin: int = 10

    fps: int = 60


class GeoNetEngine:
    def __init__(self, config: GeoNetConfig | None = None) -> None:
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

        self._grid = PatchesGrid(
            screen_width=self._cfg.screen_width,
            screen_height=self._cfg.screen_heigth,
            grid_size=self._cfg.grid_size,
            grid_margin=self._cfg.grid_margin,
        )
        self._sensor_manager = SensorManager(self._grid)

    def _handle_events(self) -> None:
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
                        print(f"Clicked grid position: {grid_pos}")

    def _update(
        self, update_fn: Callable[[SensorManager, PatchesGrid], None] | None
    ) -> None:
        if update_fn is not None:
            update_fn(self._sensor_manager, self._grid)
        self._sensor_manager._update()

    def _draw(self) -> None:
        self._screen.fill(Color.BLACK.to_tuple())
        self._grid._draw(self._screen)
        self._sensor_manager._draw(self._screen)
        pygame.display.flip()

    def main_loop(
        self,
        setup_fn: Callable[[SensorManager, PatchesGrid], None] | None = None,
        update_fn: Callable[[SensorManager, PatchesGrid], None] | None = None,
    ) -> None:
        if setup_fn is not None:
            setup_fn(self._sensor_manager, self._grid)
        last_draw_time = pygame.time.get_ticks()
        first_draw = True
        while not self._quit:
            self._handle_events()

            # Only execute every second (1000 milliseconds)
            current_time = pygame.time.get_ticks()
            if current_time - last_draw_time >= 1000 or first_draw:
                self._update(update_fn)
                self._draw()
                last_draw_time = current_time
                first_draw = False
            self._clock.tick(self._cfg.fps)

        pygame.quit()
