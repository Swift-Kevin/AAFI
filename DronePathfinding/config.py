from enum import Enum

WINDOW_SIZE = 750
GRID_SIZE = 250
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
MENU_HEIGHT = 30
SPEED = 20
WINDOW_HEIGHT = WINDOW_SIZE + MENU_HEIGHT

C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_GRAY = (100, 100, 100)
C_DARKGRAY = (40, 40, 40)
C_GREEN = (50, 160, 70)
C_BLUE = (50, 120, 220)
C_DARKBLUE = (25, 60, 110)
C_YELLOW = (230, 210, 120)
C_BROWN = (150, 100, 50)
C_ORANGE = (255, 165, 0)
C_RED = (200, 50, 50)
C_CYAN = (0, 255, 255)
C_PURPLE = (180, 100, 200)

START_COLOR    = C_PURPLE
END_COLOR      = C_RED
DRONE_COLOR    = C_ORANGE
PATH_COLOR     = C_CYAN
MENU_BG_COLOR  = (200, 200, 200)
MENU_TEXT_COLOR = C_BLACK

class Terrain(Enum):
    DEEPWATER = 0
    WATER = 0
    SAND  = 1
    DIRT  = 2
    GRASS = 3
    ROCK  = 4

TERRAIN_PROPERTIES = {
    "deepwater": {"walkable": False, "weight": 9999, "color": C_DARKBLUE},
    "water": {"walkable": False, "weight": 9999, "color": C_BLUE},
    "sand":  {"walkable": True,  "weight": 15,  "color": C_YELLOW},
    "dirt":  {"walkable": True,  "weight": 5,   "color": C_BROWN},
    "grass": {"walkable": True,  "weight": 1,   "color": C_GREEN},
    "rocks": {"walkable": True,  "weight": 20,  "color": C_GRAY},
}

TERRAIN_CYCLE = ["deepwater", "water", "sand", "dirt", "grass", "rocks"]

TERRAIN_PARAMS = {
    "scale": 10,
    "octaves": 4,
    "persistence": 0.25,
    "lacunarity": 2
}
