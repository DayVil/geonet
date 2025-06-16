"""
GeoNet - A Sensor Network Simulation Framework

GeoNet is a comprehensive Python framework for simulating wireless sensor networks
with spatial grid-based environments. It provides tools for creating sensor networks,
managing connections, and visualizing network behavior in real-time.

Main Components:
    engine: Core simulation engine and visualization components
        - geonet: Main simulation engine and configuration
        - grid: Spatial grid system for environmental representation
        - geo_color: Color definitions and utilities

    components: Core simulation components
        - sensors: Sensor classes and management utilities
        - coords: Coordinate system and spatial calculations

Features:
    - Real-time visualization using pygame
    - Flexible sensor network topologies (mesh, chain, star, custom)
    - Environmental sensing and measurement
    - Inter-sensor communication simulation
    - Grid-based spatial representation
    - Configurable simulation parameters

Example Usage:
    ```python
    from src.engine.geonet import GeoNetEngine, GeoNetConfig
    from src.components.sensors.sensor_manager import SensorManager

    # Create engine with custom configuration
    config = GeoNetConfig(screen_width=1200, grid_size=60)
    engine = GeoNetEngine(config)

    # Define setup and update functions
    def setup(sensor_manager, grid):
        # Create sensors and set up network
        sensors = sensor_manager.create_and_append_sensors(10, initial_state=0.0)
        sensor_manager.connect_sensors_mesh(sensors)
        return {"tick": 0}

    def update(sensor_manager, grid, global_state):
        # Update simulation logic
        global_state["tick"] += 1
        return global_state

    # Run simulation
    engine.main_loop(setup_fn=setup, update_fn=update)
    ```

Authors: GeoNet Development Team
License: See LICENSE file
Version: See pyproject.toml
"""

# Main package imports for convenience
from src.components.coords.coordinates import Coordinates
from src.engine.geo_color import Color
from src.engine.geonet import GeoNetConfig, GeoNetEngine
from src.engine.grid import PatchesGrid


__all__ = [
    "GeoNetEngine",
    "GeoNetConfig",
    "PatchesGrid",
    "Color",
    "Coordinates",
]
