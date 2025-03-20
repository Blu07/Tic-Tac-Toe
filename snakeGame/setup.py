import pygame
from pygame.math import Vector2


# PyGame Setup

pygame.init()

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

FPS = 120 # Render screen at this rate
TPS = 5 # Update game (tick) at this rate


# Main Setup

GRID_CELLS_X = 30
GRID_CELLS_Y = 14

INIT_PLAYER_X: int = GRID_CELLS_X // 2
INIT_PLAYER_Y: int = GRID_CELLS_Y // 2
INIT_LENGTH: int = 5
INIT_COLOR: str = "blue"
INIT_DIR: Vector2 = Vector2(1, 0)


GRID_PADDING_X = 100
GRID_PADDING_Y = 200

CELL_SIZE = (WINDOW_WIDTH - 200) // GRID_CELLS_X


# Structs Setup

SNAKE_TEXTURE_PACK = "snake"

FOOD_TEXTURE_PACK = "food"
RANDOM_FOOD_MAX_ATTEMPTS = 100000

HOTSPOT_TEXTURE_PACK = "hotSpots"


# Loops Setup

# - Game Over Screen

GO_BG_COLOR = "aquamarine"

# -- Title Text
GO_TITLE = "You Died!"
GO_TITLE_COLOR = "brown3"
GO_TITLE_FONT = pygame.font.Font(None, 74)

# -- Start Button
GO_RESTART_BUTTON_TEXT = "Click to Restart Game"
GO_RESTART_BUTTON_COLOR = (0, 128, 255)
GO_RESTART_BUTTON_TEXT_COLOR = (255, 255, 255)
GO_RESTART_BUTTON_FONT = pygame.font.Font(None, 24)
GO_RESTART_BUTTON_PADDING = Vector2(50, 30)

# - Start Screen
S_BG_COLOR = "aquamarine"

# Title Text
S_TITLE = "Welcome To Snake!"
S_TITLE_COLOR = "brown3"
S_TITLE_FONT = pygame.font.Font(None, 74)

# Start Button
S_START_BUTTON_TEXT = "Click to Start Game"
S_START_BUTTON_COLOR = (0, 128, 255)
S_START_BUTTON_TEXT_COLOR = (255, 255, 255)
S_START_BUTTON_FONT = pygame.font.Font(None, 24)
S_START_BUTTON_PADDING = Vector2(50, 30)
    
    

# - Gameplay Screen

GP_BACKGROUND_COLOR = "gray"