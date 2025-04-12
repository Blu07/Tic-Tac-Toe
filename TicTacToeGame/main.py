import pygame

from copy import deepcopy

from common.grid import Grid
from common.setup import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_BORDER_WIDTH, GRID_PADDING_LEFT, GRID_PADDING_RIGHT, GRID_PADDING_TOP, GRID_PADDING_BOTTOM

from .structs import Board
from .loops import gameOverLoop, gameplayLoop, settingsLoop
from .setup import INIT_SETTINGS


def mainTTTLoop(window: pygame.Surface, clock: pygame.time.Clock) -> None:
    """ Main loop for the Tic Tac Toe game.
    
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock object.
    """    

    initPlayer = 1
    settings = deepcopy(INIT_SETTINGS)
    
    while True:
        
        # Set up settings
        settings, navigation = settingsLoop(window, clock, initSettings=settings)
        if navigation == "menu":
            return

        pygame.display.set_caption("Playing Tic Tac Toe")
        
        players = {
            -1: settings["playerO"],
            1: settings["playerX"]
        }

        winLength = settings["win_length"]
        numCellsX = settings["grid_size_x"]
        numCellsY = settings["grid_size_y"]
        
        cellSizePX = min(
            (WINDOW_WIDTH - GRID_PADDING_RIGHT - GRID_PADDING_LEFT) // numCellsX,
            (WINDOW_HEIGHT - GRID_PADDING_TOP - GRID_PADDING_BOTTOM) // numCellsY
        )
        
        # totalCombinations = generateCombinationMap(xCells=numCellsX, yCells=numCellsY, winLength=winLength)
        
        windowPosX = (WINDOW_WIDTH - numCellsX * cellSizePX + 2 * GRID_BORDER_WIDTH) / 2 # Center the grid on the window in the X direction
        grid = Grid(windowPosX, GRID_PADDING_TOP, numCellsX, numCellsY, cellSizePX)
        board = Board(grid, winLength, initPlayer)
        
        
        result = gameplayLoop(window, grid, board, initPlayer, players, clock)
        
        gameOverLoop(window, True, clock, result)
        
        # Switch starting player
        initPlayer = -initPlayer
