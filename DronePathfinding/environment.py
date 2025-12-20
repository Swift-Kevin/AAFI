import numpy as np
import noise
from config import *

class Cell:
    def __init__(self, terrain: str):
        self.terrain: str = terrain
        self.walkable: bool = TERRAIN_PROPERTIES[terrain]["walkable"]
        self.weight: float = TERRAIN_PROPERTIES[terrain]["weight"]
        self.color: tuple[int,int,int] = TERRAIN_PROPERTIES[terrain]["color"]

def generate_terrain() -> tuple[np.ndarray, np.ndarray]:
    terrain_grid: np.ndarray = np.empty((GRID_SIZE, GRID_SIZE), dtype=object)
    base_heights: np.ndarray = np.zeros((GRID_SIZE, GRID_SIZE))
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            nx, ny = x / GRID_SIZE, y / GRID_SIZE
            height = noise.pnoise2(
                nx * TERRAIN_PARAMS["scale"],
                ny * TERRAIN_PARAMS["scale"],
                octaves=TERRAIN_PARAMS["octaves"],
                persistence=TERRAIN_PARAMS["persistence"],
                lacunarity=TERRAIN_PARAMS["lacunarity"],
                repeatx=1024,
                repeaty=1024,
                base=42
            )
            base_heights[y, x] = height
            terrain_grid[y, x] = Cell(height_to_terrain(height))
    return terrain_grid, base_heights

def height_to_terrain(height: float) -> str:
    if height < -0.7: return "deepwater"
    if height < -0.2: return "water"
    if height < -0.1: return "sand"
    if height < 0.1: return "dirt"
    if height < 0.4: return "grass"
    return "rocks"
