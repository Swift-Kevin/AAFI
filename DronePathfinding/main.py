from visualizer import *
from helper import *
from config import *
import pygame
from typing import Optional

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + MENU_HEIGHT))
pygame.display.set_caption("Drone Simulator")

start: Optional[Coord] = None
end: Optional[Coord] = None
path: Optional[list[Coord]] = None
path_index: int = 0
running = True
clock = pygame.time.Clock()
grid, base_heights = generate_terrain()

while running:
    dt = clock.tick(60)  # ms per frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start, end, path, path_index = evt_HandleMouse(
                event, grid, start, end, path, path_index
            )
        elif event.type == pygame.KEYDOWN:
            reset_vals = evt_HandleKey(event)
            if reset_vals:
                grid, start, end, path, path_index = reset_vals

    if path:
        path_index = updateDrone(path, path_index, dt, SPEED)
        drone_pos = path[path_index]
    else:
        drone_pos = None

    screen.fill(C_WHITE)
    DrawMenubar(screen, start, end, path, path_index)
    y_offset = MENU_HEIGHT
    DrawGrid(screen, grid, y_offset)
    DrawPath(screen, path, y_offset)
    DrawStartEnd(screen, start, end, y_offset)

    if drone_pos:
        r, c = drone_pos
        pygame.draw.rect(screen, DRONE_COLOR, (c * CELL_SIZE, r * CELL_SIZE + y_offset, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()

pygame.quit()
