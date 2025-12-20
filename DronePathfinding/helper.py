from a_star import A_StarPather
from environment import generate_terrain, Cell
from config import *
import pygame
import numpy as np
from typing import Optional, Tuple, List

Coord = Tuple[int,int]

def recalculatePath(grid: np.ndarray, start: Coord, end: Coord):
    if start and end:
        path = A_StarPather(grid, start, end)
        if path:
            return path, 0
    return None, 0

def getMousedCell(pos: tuple[int,int], offset_y: int = MENU_HEIGHT) -> Optional[Coord]:
    x, y = pos
    if y < offset_y: return None
    cell_pixel_size = WINDOW_SIZE / GRID_SIZE
    row = min(int((y - offset_y) / cell_pixel_size), GRID_SIZE-1)
    col = min(int(x / cell_pixel_size), GRID_SIZE-1)
    return row, col

def evt_HandleMouse(event, grid, start, end, path=None, path_index=0):
    cell_pos = getMousedCell(pygame.mouse.get_pos())
    if not cell_pos: return start, end, path, path_index
    row, col = cell_pos
    cell = grid[row][col]
    if event.button == 1 and cell.walkable: start = (row, col)
    elif event.button == 3 and cell.walkable: end = (row, col)
    if start and end:
        path, path_index = recalculatePath(grid, start, end)
    return start, end, path, path_index

def evt_HandleKey(event):
    if event.key == pygame.K_r: return generate_terrain(), None, None, None
    return None

def updateDrone(path: Optional[List[Coord]], path_index: int, dt: float, speed: float):
    if not path or path_index is None:
        return path_index
    dt_accum = getattr(updateDrone, "accumulator", 0.0)
    dt_accum += dt
    move_delay = 1000 / speed
    if dt_accum >= move_delay:
        path_index += 1
        dt_accum = 0.0
    updateDrone.accumulator = dt_accum
    if path_index >= len(path):
        path_index = len(path) - 1
    return path_index
