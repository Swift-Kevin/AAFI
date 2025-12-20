import heapq
from config import *
from typing import Optional, Tuple, List, Dict
import numpy as np

Coord = Tuple[int,int]

class A_StarPather:
    def __new__(cls, grid: np.ndarray, start: Coord, goal: Coord) -> Optional[List[Coord]]:
        return cls.find_path(grid, start, goal)

    @staticmethod
    def heuristic(a: Coord, b: Coord) -> float:
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    @staticmethod
    def get_neighbors(node: Coord, grid: np.ndarray):
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = node[0]+dy, node[1]+dx
            if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE:
                if grid[ny][nx].walkable:
                    yield ny, nx

    @staticmethod
    def reconstruct_path(came_from: Dict[Coord, Coord], current: Coord) -> List[Coord]:
        path: List[Coord] = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    @staticmethod
    def find_path(grid: np.ndarray, start: Coord, goal: Coord) -> Optional[List[Coord]]:
        if not grid[start[0]][start[1]].walkable or not grid[goal[0]][goal[1]].walkable:
            return None

        open_set: list[tuple[float, Coord]] = [(0, start)]
        came_from: dict[Coord, Coord] = {}
        g_score: dict[Coord, float] = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return A_StarPather.reconstruct_path(came_from, current)
            for neighbor in A_StarPather.get_neighbors(current, grid):
                tentative_g = g_score[current] + grid[neighbor[0]][neighbor[1]].weight
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + A_StarPather.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))
        return None
