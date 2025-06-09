from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from dataclasses import dataclass

import pygame

from src.components.sensor_manager import SensorManager
from src.engine.grid import PatchesGrid


@dataclass(frozen=True)
class GeoNetConfig:
    screen_width: int = 1000
    screen_heigth: int = 800

    grid_size: int = 40
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

    def _update(self) -> None:
        self._sensor_manager._update()

    def _draw(self) -> None:
        self._screen.fill((20, 20, 20))
        self._grid._draw(self._screen)
        self._sensor_manager._draw(self._screen)
        pygame.display.flip()

    def main_loop(
        self, base_scenario: Callable[[SensorManager, PatchesGrid], None]
    ) -> None:
        base_scenario(self._sensor_manager, self._grid)
        last_draw_time = pygame.time.get_ticks()
        first_draw = True
        while not self._quit:
            self._handle_events()

            # Only execute every second (1000 milliseconds)
            current_time = pygame.time.get_ticks()
            if current_time - last_draw_time >= 1000 or first_draw:
                self._update()
                self._draw()
                last_draw_time = current_time
                first_draw = False
            self._clock.tick(self._cfg.fps)

        pygame.quit()
