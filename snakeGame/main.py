import pygame

from copy import deepcopy

from common.grid import Grid
from common.setup import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_BORDER_WIDTH, GRID_PADDING_LEFT, GRID_PADDING_RIGHT, GRID_PADDING_TOP, GRID_PADDING_BOTTOM

from .structs import FoodList, Snake, HotSpotList
from .loops import gameplayLoop, gameOverLoop, settingsLoop
from .setup import INIT_SETTINGS, INIT_LENGTH


def mainSnakeLoop(window: pygame.Surface, clock: pygame.time.Clock) -> None:
    """ Main loop for the Snake game.
    
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock object.
    """
    
    settings = deepcopy(INIT_SETTINGS)

    # Main Game Loop
    while True:
        
        # Set up settings
        settings, navigation = settingsLoop(window, clock, settings)
        
        if navigation == "menu":
            return # Return to main menu
        
        
        pygame.display.set_caption("Playing Snake")
        
        numCellsX = settings['grid_size_x']
        numCellsY = settings['grid_size_y']
        
        initPlayerX = numCellsX // 2
        initPlayerY = numCellsY // 2
        
        initLength = min(initPlayerX+1, INIT_LENGTH) # Limit the snakes length to fit the board when starting
        
        cellSizePX = min(
            (WINDOW_WIDTH - GRID_PADDING_RIGHT - GRID_PADDING_LEFT) // numCellsX,
            (WINDOW_HEIGHT - GRID_PADDING_TOP - GRID_PADDING_BOTTOM) // numCellsY
        )
        
        windowPosX = (WINDOW_WIDTH - numCellsX * cellSizePX + 2 * GRID_BORDER_WIDTH) / 2 # Center the grid on the window in the X direction

        # Initialize new game objects every loop
        grid = Grid(windowPosX, GRID_PADDING_TOP, numCellsX, numCellsY, cellSizePX)
        foodList = FoodList(window, grid)
        hotSpotList = HotSpotList(window, grid, threshold=3)
        snake = Snake(window, grid, foodList, hotSpotList, initPlayerX, initPlayerY, initLength)
        
        # Show Screens
        result = gameplayLoop(window, snake, grid, foodList, hotSpotList, clock)
        
        gameOverLoop(window, clock, result)

