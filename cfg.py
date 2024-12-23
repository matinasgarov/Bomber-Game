import pygame 

# Colors
COLOR_BACKGROUND = (27, 27, 27)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
TEXT_COLOR = COLOR_WHITE  # Example color for text in the game
PAUSE_BACKGROUND_COLOR = (0, 0, 0)  # Dark grey color for pause menu background

# Menu config
MENU_FPS = 60.0
MENU_BACKGROUND_COLOR = (0, 0, 0)
MENU_TITLE_COLOR = (220, 20, 60)

# Window config
WINDOW_SCALE = 0.75
WINDOW_SIZE_PERC = 0.6
TILES_NUM = 13
pygame.display.init()
INFO = pygame.display.Info()
min_size = min(INFO.current_h, INFO.current_w)
WINDOW_SIDE_SIZE = int(min_size * WINDOW_SIZE_PERC)
WINDOW_SIZE = (WINDOW_SIDE_SIZE, WINDOW_SIDE_SIZE)
TILE_SIZE = int(WINDOW_SIDE_SIZE / TILES_NUM)

# Font config
FONT_TYPE = 'Bebas-Regular'
FONT_SIZE = 60
FONT_SIZE_LARGE = 80  # Larger font size for pause menu titles

# Game config
FPS = 60  # Frames per second
GAME_SPEED = 17
GAME_SPEED_AI_ONLY = 60
GAME_BACKGROUND = (107, 142, 35)

BOMB_TIME = 3000  # ms

FONT_TYPE = 'Bebas-Regular'
FONT_SIZE = 60
TEXT_LOSE = 'GAME OVER'
TEXT_WIN = 'WIN'
GRID = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]