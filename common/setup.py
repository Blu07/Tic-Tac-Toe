import pygame
from pygame.math import Vector2

pygame.init() # Initialize Pygame to use Font and other Pygame features

FPS = 120 # Render screen at this rate

# Start Screen (Prefix S)
# -- Window
WINDOW_WIDTH: int = 1200
WINDOW_HEIGHT: int = 1000

CENTER = Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

BG_COLOR = "aquamarine"
GAMEPLAY_BG_COLOR = "gray"


# FOLDER PATHS
TEXTURES_FOLDER: str = "_textures"


# GRID
GRID_COLORS = ["burlywood2", "burlywood3"]
GRID_BORDER_WIDTH = 4 #px
GRID_BORDER_COLOR: str = "black"


GRID_PADDING_LEFT = 100
GRID_PADDING_RIGHT = 100
GRID_PADDING_TOP = 200
GRID_PADDING_BOTTOM = 100

