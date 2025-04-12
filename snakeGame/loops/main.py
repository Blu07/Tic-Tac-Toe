import pygame

from copy import deepcopy

from common.grid import Grid
from common.setup import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_BORDER_WIDTH, GRID_PADDING_LEFT, GRID_PADDING_RIGHT, GRID_PADDING_TOP, GRID_PADDING_BOTTOM

from ..structs import FoodList, Snake, HotSpotList
from .game_over import gameOverLoop
from .gameplay import gameplayLoop
from .win import winLoop
from ..setup import INIT_SETTINGS, INIT_PLAYER_X, INIT_PLAYER_Y, INIT_LENGTH


def mainSnakeLoop(window: pygame.Surface, clock: pygame.time.Clock) -> None:
    """ Main loop for the Snake game.
    
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock object.
    """
    
    pygame.display.set_caption("Snake")
    

    # Main Game Loop
    while True:
        
        # Set up settings
        # settings = setSettings(window, clock) # TODO: Implement settings screen
        # pygame.display.set_caption("Playing Snake")
        
        settings = deepcopy(INIT_SETTINGS)
        numCellsX = settings['grid_size_x']
        numCellsY = settings['grid_size_y']

        cellSizePX = min(
            (WINDOW_WIDTH - GRID_PADDING_RIGHT - GRID_PADDING_LEFT) // numCellsX,
            (WINDOW_HEIGHT - GRID_PADDING_TOP - GRID_PADDING_BOTTOM) // numCellsY
        )
        
        # Initialize new game objects every loop
        grid = Grid(GRID_PADDING_LEFT, GRID_PADDING_TOP, numCellsX, numCellsY, cellSizePX)
        foodList = FoodList(window, grid)
        hotSpotList = HotSpotList(window, grid, threshold=3)
        snake = Snake(window, grid, foodList, hotSpotList, INIT_PLAYER_X, INIT_PLAYER_Y, INIT_LENGTH)
        
        # Show Screens
        won, died = gameplayLoop(window, True, snake, grid, foodList, hotSpotList, clock)
        
        if won: winLoop(window, True, clock)
        elif died: gameOverLoop(window, True, clock)

