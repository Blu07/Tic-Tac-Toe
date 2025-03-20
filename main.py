import pygame

from common.grid import Grid

from TicTacToeGame.structs import Board, GhostShape, generateCombinationMap
from TicTacToeGame.loops import gameplayLoop, gameOverLoop
from TicTacToeGame.setup import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, GRID_BORDER_WIDTH, GRID_CELLS_X, GRID_CELLS_Y, INIT_PLAYER, INIT_PLAYER_X, INIT_PLAYER_Y, INIT_LENGTH, INIT_COLOR, INIT_DIR, TEXTURE_PACK, GRID_PADDING_X, GRID_PADDING_TOP, GRID_PADDING_BOTTOM, CELL_SIZE, WIN_LENGTH, MAX_WIN_LENGTH


# pygame

pygame.display.set_caption("Tic Tac Toe")

clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

initPlayer = INIT_PLAYER
winLength = WIN_LENGTH
numCellsX = GRID_CELLS_X
numCellsY = GRID_CELLS_Y


while True:
    CELL_SIZE_PX = min((WINDOW_WIDTH - GRID_PADDING_X*2) // GRID_CELLS_X, (WINDOW_HEIGHT - GRID_PADDING_TOP - GRID_PADDING_BOTTOM) // numCellsY)
    
    
    totalCombinations = generateCombinationMap(xCells=numCellsX, yCells=numCellsY, winLength=winLength)

    
    windowPosX = (WINDOW_WIDTH - numCellsX * CELL_SIZE_PX + 2 * GRID_BORDER_WIDTH) / 2 # Center the grid on the window in the X direction
    grid = Grid(windowPosX, GRID_PADDING_TOP, numCellsX, numCellsY, CELL_SIZE_PX)
    board = Board(grid, TEXTURE_PACK, winLength, INIT_PLAYER, totalCombinations)
    ghostShape = GhostShape(CELL_SIZE_PX, initPlayer, TEXTURE_PACK)
    result = gameplayLoop(window, grid, board, ghostShape, initPlayer, clock)
    
    if result != 0:
        # numCellsX += 1
        # numCellsY += 1
        # winLength = min((numCellsX-1) // 2 + 1, numCellsX - 1) + 1 # regulate the win length based on the grid size in the X direction.
        initPlayer = result # The winner starts the next game
    else:
        initPlayer = INIT_PLAYER
        winLength = WIN_LENGTH
        numCellsX = GRID_CELLS_X
        numCellsY = GRID_CELLS_Y
        
    
    gameOverLoop(window, True, clock, result)



pygame.quit()

