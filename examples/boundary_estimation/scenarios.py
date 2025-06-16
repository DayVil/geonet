from collections.abc import Callable
import random

from src.components.coords.coordinates import Coordinates
from src.engine.geo_color import Color
from src.engine.grid import PatchesGrid


def _scen1(patches: PatchesGrid):
    patches.set_color_rect(
        starting_point=Coordinates(12, 25),
        width=35,
        height=15,
        color=Color.NAVY,
    )
    patches.set_color_rect(
        starting_point=Coordinates(15, 22),
        width=25,
        height=20,
        color=Color.NAVY,
    )
    patches.set_color_rect(
        starting_point=Coordinates(20, 10),
        width=25,
        height=20,
        color=Color.NAVY,
    )


def _scen2(patches: PatchesGrid):
    patches.set_color_rect(Coordinates(3, 4), width=30, height=20, color=Color.NAVY)
    patches.set_color_rect(Coordinates(23, 10), width=20, height=25, color=Color.NAVY)


def _scen3(patches: PatchesGrid):
    patches.set_color_rect(Coordinates(10, 30), width=20, height=3, color=Color.NAVY)
    patches.set_color_rect(Coordinates(15, 27), width=20, height=7, color=Color.NAVY)

    patches.set_color_rect(Coordinates(30, 20), width=20, height=30, color=Color.NAVY)
    patches.set_color_rect(Coordinates(12, 15), width=10, height=20, color=Color.NAVY)


def _scen4(patches: PatchesGrid):
    patches.set_color_rect(Coordinates(2, 20), width=20, height=3, color=Color.NAVY)
    patches.set_color_rect(Coordinates(12, 17), width=20, height=3, color=Color.NAVY)
    patches.set_color_rect(Coordinates(16, 17), width=10, height=20, color=Color.NAVY)

    patches.set_color_rect(Coordinates(20, 20), width=20, height=20, color=Color.NAVY)
    patches.set_color_rect(Coordinates(22, 15), width=18, height=30, color=Color.NAVY)


def _scen5(patches: PatchesGrid):
    patches.set_color_rect(Coordinates(2, 2), width=20, height=30, color=Color.NAVY)
    patches.set_color_rect(Coordinates(30, 10), width=15, height=35, color=Color.NAVY)


def load_random_scenario(patches: PatchesGrid) -> None:
    scenarios: list[Callable[[PatchesGrid], None]] = [
        _scen1,
        _scen2,
        _scen3,
        _scen4,
        _scen5,
    ]

    scen = random.choice(scenarios)
    scen(patches)
