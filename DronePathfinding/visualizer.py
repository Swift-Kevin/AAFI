import pygame
from config import *

def _cell_rect(r, c, offset_y=0):
    size = WINDOW_SIZE / GRID_SIZE
    return pygame.Rect(int(c * size), int(r * size + offset_y), int(size), int(size))

def DrawGrid(screen, grid, offset_y=0):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            cell = grid[r][c]
            pygame.draw.rect(screen, cell.color, _cell_rect(r, c, offset_y))

def DrawPath(screen, path, offset_y=0):
    if path:
        for r, c in path:
            pygame.draw.rect(screen, PATH_COLOR, _cell_rect(r, c, offset_y))

def DrawStartEnd(screen, start, end, offset_y=0):
    if start:
        pygame.draw.rect(screen, START_COLOR, _cell_rect(*start, offset_y))
    if end:
        pygame.draw.rect(screen, END_COLOR, _cell_rect(*end, offset_y))

def DrawDrone(screen, drone_pos, offset_y=0):
    if drone_pos:
        r, c = drone_pos
        size = WINDOW_SIZE / GRID_SIZE
        cx = int(c * size + size / 2)
        cy = int(r * size + offset_y + size / 2)
        radius = max(int(size / 3), 1)
        pygame.draw.circle(screen, DRONE_COLOR, (cx, cy), radius)

def DrawMenubar(screen, start, end, path, path_index=0):
    pygame.draw.rect(screen, MENU_BG_COLOR, (0, 0, WINDOW_SIZE, MENU_HEIGHT))
    font = pygame.font.SysFont(None, 24)
    moving = False
    if path and path_index < len(path) - 1:
        moving = True
    texts = [
        f"Start: {start if start else 'None'}",
        f"End: {end if end else 'None'}",
        f"Path length: {len(path) if path else 0}",
        "Moving" if moving else "Stopped"
    ]
    col_width = WINDOW_SIZE // 4
    for i, t in enumerate(texts):
        surf = font.render(t, True, MENU_TEXT_COLOR)
        x = i * col_width + (col_width - surf.get_width()) // 2
        y = (MENU_HEIGHT - surf.get_height()) // 2
        screen.blit(surf, (x, y))
