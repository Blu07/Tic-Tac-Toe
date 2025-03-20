import pygame
from pygame.math import Vector2

from common.setup import GRID_COLORS, GRID_BORDER_WIDTH, GRID_BORDER_COLOR
from .utils import isOutOfBounds

class Grid():
    
    borderWidthPX = GRID_BORDER_WIDTH
    colors = GRID_COLORS
    borderColor = GRID_BORDER_COLOR
    
    def __init__(self, windowPosX: int, windowPosY: int, numCellsX: int, numCellsY: int, cellSizePX: int):
        """
        Initializes a Grid object. The grid is used to represent the game area.
        The grid stores grid properties and does not contain any game logic.

        Args:
            screenPosX: The x-coordinate position of the grid on the screen.
            screenPosY: The y-coordinate position of the grid on the screen.
            numCellsX: The number of cells in the x-direction of the grid (default is 30).
            numCellsY: The number of cells in the y-direction of the grid (default is 20).
            cellSize: The size of each cell in pixels (default is 20).
        """
        
        self.windowPosX = windowPosX
        self.windowPosY = windowPosY        
        self.numCellsX = numCellsX
        self.numCellsY = numCellsY
        self.cellSizePX = cellSizePX
        
        
        self.grid = [[(x+y)%2 for x in range(numCellsX)] for y in range(numCellsY)]
        
        # The grid surface size includes the border, so add twice the border width (left + right, or top + bottom)
        surfaceWidth = numCellsX * cellSizePX + 2 * self.borderWidthPX
        surfaceHeight = numCellsY * cellSizePX + 2 * self.borderWidthPX
        
        # Create a background surface for the grid (including the border space)
        # Draw the grid onto the gridSurface once
        self.gridSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.drawGrid()
    
    
    
    
    def isOutOfBounds(self, action: Vector2):
        """Check if a given position (Vector2) is outside the grid"""
        return isOutOfBounds(action, self.numCellsX, self.numCellsY)
    
    
    
    def drawGrid(self):
        """ Draws the grid onto the gridSurface, to be reused every frame. """
        # Draw the border around the grid
        gridWidth = self.cellSizePX * self.numCellsX
        gridHeight = self.cellSizePX * self.numCellsY
        
        # The grid's total area includes the border, so draw the border at (0, 0) on the gridSurface
        borderRect = (0, 0, gridWidth + 2 * self.borderWidthPX, gridHeight + 2 * self.borderWidthPX)
        pygame.draw.rect(self.gridSurface, self.borderColor, borderRect, self.borderWidthPX)
        
        # Draw the alternating grid colors
        for y, xList in enumerate(self.grid):
            for x, num in enumerate(xList):
                color = self.colors[num]
                rect = self.getRectFromGridPos(Vector2(x, y))  # This rect is relative to gridSurface
                pygame.draw.rect(self.gridSurface, color, rect)
    
    
    def getRectFromGridPos(self, gridPos: Vector2) -> set:
        """
        Returns the rectangle coordinates on the window corresponding to the given grid position.
        
        Args:
            gridPos (Vector2): The grid position (x, y) for which to calculate the rectangle coordinates.
        
        Returns:
            rect (pygame.Rect): A set containing the rectangle coordinates (windowX, windowY, width, height).
        """

        windowX = self.cellSizePX * gridPos.x + self.borderWidthPX  # Offset by borderWidth
        windowY = self.cellSizePX * gridPos.y + self.borderWidthPX  # Offset by borderWidth
        return pygame.Rect(windowX, windowY, self.cellSizePX, self.cellSizePX)

    
    def getGridPosFromWindowPos(self, windowPos: Vector2) -> Vector2:
        """
        Converts a window position to a grid position.
        Args:
            windowPos (Vector2): The window position to convert.
        Returns:
            Vector2: The corresponding grid position.
        """
        
        gridX = (windowPos.x - self.windowPosX - self.borderWidthPX) // self.cellSizePX
        gridY = (windowPos.y - self.windowPosY - self.borderWidthPX) // self.cellSizePX
        gridPos = Vector2(gridX, gridY)
        
        return gridPos
    
    def getWindowPosFromGridPos(self, gridPos: Vector2) -> Vector2:
        """
        Converts a grid position to a window position.
        Args:
            gridPos (Vector2): The grid position to convert.
        Returns:
            Vector2: The corresponding window position.
        """
        
        windowX: int = self.windowPosX + self.cellSizePX * gridPos.x + self.borderWidthPX
        windowY: int = self.windowPosY + self.cellSizePX * gridPos.y + self.borderWidthPX
        windowPos: Vector2 = Vector2(windowX, windowY)
        
        return windowPos
    
    
    def draw(self, window: pygame.Surface):
        """ Blits the pre-drawn gridSurface onto the window at the correct position. """
        window.blit(self.gridSurface, (self.windowPosX, self.windowPosY))

