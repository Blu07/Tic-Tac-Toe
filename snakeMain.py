import pygame

from common.grid import Grid

from snakeGame.structs import FoodList, Snake, HotSpotList
from snakeGame.loops import gameplayLoop, gameOverLoop, startScreenLoop, winLoop
from snakeGame.setup import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GRID_CELLS_X, GRID_CELLS_Y, INIT_PLAYER_X, INIT_PLAYER_Y, INIT_LENGTH, INIT_COLOR, INIT_DIR, GRID_PADDING_X, GRID_PADDING_Y, CELL_SIZE


# pygame

pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CELL_SIZE = (WINDOW_WIDTH - 200) // GRID_CELLS_X


# Show Start Screen first
startScreenLoop(window, True, clock)

# Main Game Loop
while True:
    # Initialize new game objects every loop
    grid = Grid(GRID_PADDING_X, GRID_PADDING_Y, GRID_CELLS_X, GRID_CELLS_Y, CELL_SIZE)
    foodList = FoodList(window, grid)
    hotSpotList = HotSpotList(window, grid, threshold=3)
    
    snake = Snake(window, grid, foodList, hotSpotList, INIT_PLAYER_X, INIT_PLAYER_Y, INIT_LENGTH, INIT_DIR, INIT_COLOR)
    
    # Show Screens
    won, died = gameplayLoop(window, True, snake, grid, foodList, hotSpotList, clock)
    
    if won:
        winLoop(window, True, clock)
        
    if died:
        gameOverLoop(window, True, clock)
