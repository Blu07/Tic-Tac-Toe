import pygame
from common.grid import Grid

from copy import deepcopy

from common.setup import WINDOW_WIDTH, WINDOW_HEIGHT, GRID_BORDER_WIDTH, GRID_PADDING_LEFT, GRID_PADDING_RIGHT, GRID_PADDING_TOP, GRID_PADDING_BOTTOM
from TicTacToeGame.setup import INIT_SETTINGS
from TicTacToeGame.structs import Board
from .game_over import gameOverLoop
from .gameplay import gameplayLoop
from .settings import setSettings


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
        settings = setSettings(window, clock, initSettings=settings)

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
