from pprint import pprint
import numpy as np
import pygame
from pygame import Vector2
import copy

from setup import GHOST_SHAPE_SIZE_FACTOR


class Grid:
    
    borderWidthPX: int = 4
    colors = ["burlywood2", "burlywood3"]
    
    
    def __init__(self, windowPosX, windowPosY, cellSizePX, numCellsX: int = 3, numCellsY: int = 3):
        
        self.windowPosX = windowPosX
        self.windowPosY = windowPosY
        self.numCellsX = numCellsX
        self.numCellsY = numCellsY
        self.cellSizePX = cellSizePX
        
        self.color = 'black'
        
        # Alternating grid of 1's and 0's to display the two colors
        self.grid = [[(x+y)%2 for x in range(numCellsX)] for y in range(numCellsY)]
        
        # The grid surface size includes the border, so add twice the border width (left + right, or top + bottom)
        surfaceWidth = numCellsX * cellSizePX + 2 * self.borderWidthPX
        surfaceHeight = numCellsY * cellSizePX + 2 * self.borderWidthPX
        
        
        # The gridSurface will be the background texture of the window.
        # Draw it once and re-use every frame
        self.gridSurface = pygame.Surface((surfaceWidth, surfaceHeight))
        self.drawGrid()
        
    
    
    def isOutOfBounds(self, action: Vector2):
        """Check if a given position (Vector2) is outside the grid"""
        return action.x < 0 or action.x >= self.numCellsX or action.y < 0 or action.y >= self.numCellsY

    
    
    
    def drawGrid(self):
        """ Draws the grid onto the gridSurface, to be reused every frame. """
        # Draw the border around the grid
        gridWidth = self.cellSizePX * self.numCellsX
        gridHeight = self.cellSizePX * self.numCellsY
        
        # The grid's total area includes the border, so draw the border at (0, 0) on the gridSurface
        borderRect = (0, 0, gridWidth + 2 * self.borderWidthPX, gridHeight + 2 * self.borderWidthPX)
        pygame.draw.rect(self.gridSurface, self.color, borderRect, self.borderWidthPX)
        
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



class Board:
    
    r1 = Vector2([-1, -1]) # Horizontal up left
    r2 = Vector2([0, -1]) # Up
    r3 = Vector2([1, -1]) # Horizontal up right
    r4 = Vector2([1, 0]) # right
    
    dirVectors = [r1, r2, r3, r4]
    
    def __init__(self, grid: Grid, texturePack, winLength: int = 3, startPlayer: int = 1, combinations: list[list[int]] = None, state = None):
        
        self.grid = grid 
        self.winLength = winLength
        self.combinations = combinations
        self.startPlayer = startPlayer
        
        self.texturePack = texturePack
        
        # Initialize the board with all zeros with correct dimensions
        self.state = [ [0] * grid.numCellsX for _ in range(grid.numCellsY) ] if state is None else state
        

    def checkHasWon(self, action: Vector2, player: int, state = None):
        
        if state is None: state = self.state
        
        for i, r in enumerate(self.dirVectors):
            # TODO: Use i to calculate if there is any possibility for the diagonals to be valid (i=0, i=2) in the corners.
            # Possible early return to save computation time over a small arithmetic calculation
            
            # print("new direction")            
            checkPos = Vector2([action.x, action.y])
            
            inverted = False
            equal = True
            equalCount = 1 # The initial position has a valid value
            
            while equal:

                # print("r:", r)
                checkPos += r
                
                valAtCheck = self.getValAtPos(checkPos, state)
                equal = valAtCheck == player

                # print("(", checkX, checkY, "):", valAtCheck, equal)
                
                if equal: equalCount += 1
                else:
                    if inverted: continue
                    
                    # Invert the searching direction and start searching form original position
                    # print("inverted search")
                    inverted = True
                    r *= -1
                    checkPos = Vector2([action.x, action.y])
                    equal = True
                    
                if equalCount == self.winLength: return True # player has won
                
                # print("count:", equalCount)    

      
        
        # For-loop never found a winning case, so player did not win
        return False
    
    
    def performAction(self, action: Vector2, player = 0, state = None) -> list[list[int]]:
        """ Perform an action on the board.
        Parameters:
        - action (Vector2): The position to add the player's value.
        - player (int): The player's value to add to the board.
        Returns:
        - bool: True if the action was successful, False otherwise.
        """
        
        if state is None:
            state = self.state
        else:
            state = copy.deepcopy(state)
            
        success = False # Change to true if the action was successful
        
        valueAtCell = self.getValAtPos(action, state)
        outOfBounds = self.grid.isOutOfBounds(action)
        
        if not outOfBounds and valueAtCell == 0:
            state[int(action.y)][int(action.x)] = player # Set the value at the correct index
            self.state = state
            success = True
        
        return state, success # Previous state, value not changed
    
    
    
    def getActions(self, state = None) -> list[Vector2]:
        # Return a list of actions of Vector2([x, y]) pairs
        
        # TODO: If the board is symmetrical, only return actions that result in unique new states
        ## First case: board is empty
        
        # Symmetrical by mid of x axis and mid of y axis (x and y axes might not be equal length)
        
        # maxX = xCells // 2 + 1 (include middle column if xCells is odd)
        # maxY = yCells // 2 + 1 (include middle row)
        
        
        
        
        if state is None: state = self.state
        
        actions = []
        for y, yList in enumerate(state):
            for x, val in enumerate(yList):
                action = Vector2(int(x), int(y))
                if val == 0:
                    actions.append(Vector2(action))
        
        return actions
    
    
    def getValAtPos(self, action: Vector2, state = None):
        if state is None: state = self.state
        if self.grid.isOutOfBounds(action): return 0
        else: return state[int(action.y)][int(action.x)]
        
    def isStateFull(self, state = None):
        if state is None: state = self.state
        
        for yList in state:
            for val in yList:
                if val == 0: return False
        
        return True
    
    
    def getPlayer(self, state):

        summed = sum(np.array(state).flatten())
        return self.startPlayer if summed == 0 else -self.startPlayer
    
    
    
    def Result(self, state, action, playerVal):
        
        newState = []
        for y, yList in enumerate(state):
            newList = []
            for x, val in enumerate(yList):
                if y == action.y and x == action.x:
                    newList.append(playerVal)
                else:
                    newList.append(val)
                    
            newState.append(newList)
        
        return newState
    
    def Actions(self, state):
        return self.getActions(state)
    
    def Player(self, state):
        return self.getPlayer(state)
    
          
    def minimax(self, s, player):
        
        actions = self.Actions(s)
        
        
        # if player == MAX:
        
        value = -np.inf * player

        for a in actions:
            checkState = self.Result(s, a, player)
                
            immidiateWin = self.checkHasWon(a, player, checkState)
            isDraw = self.isStateFull(checkState)
            
            if immidiateWin: return player
            if isDraw: return 0

            newValue = self.minimax(s = checkState, player = -player)
            
            if player == 1: value = max(value, newValue)
            elif player == -1: value = min(value, newValue)
                
        return value
        
        # if player == MIN:
        #     value = np.inf
        #     values = [value]
        #     for a in actions:
        #         print("\t"*tabs, "Action:", a)
        #         checkState = self.Result(s, a, player)

                    
        #         immidiateWin = self.checkHasWon(a, MIN, checkState)
        #         if immidiateWin:
        #             print("\t"*tabs, 'MIN won')
        #             return MIN
        #         if self.isStateFull(checkState):
        #             print("\t"*tabs, 'Draw')
        #             return 0

        #         newValue = self.minimax(s = checkState, player = MAX, tabs=tabs+1)
        #         values.append(newValue)
        #         value = min(value, newValue)
        #         print("\t"*tabs, 'MIN', value, values)
                
        #     return value
        
    
    
    def getBestAction(self, state, player):        
        state = copy.deepcopy(state)
        actions = self.getActions(state)
        # actions = [Vector2(2, 0)]
        
        print("finding the best action for player ", player)
        print("on state:", np.array(state).flatten())
        
        
        bestValue = -player * np.inf  # Opposite of player's goal
        bestAction = None
        
        values = []

        for action in actions:
            newState = self.Result(state, action, player)
            print("checking action:", action, "with state:")
            for yList in newState:
                print(yList)
            
            value = self.minimax(newState, -player)
            
            bestValue = max(bestValue, value) if player == 1 else min(bestValue, value)
            
            print("Value:", value, "for action:", action)
            values.append(value)


            bestAction = actions[values.index(bestValue)]
        
        print("Values:", values)
        print("Actions:", actions)
        print(f"Best value: {bestValue}, Best action: {bestAction}")
        
        return bestAction




    def evaluateState(self, state):

        # evaluationState = np.array([[ 1 if v == 0 else v for v in yList] for yList in state]) # Convert 0's to 1's to give 1 point score where empty
        evaluationState = np.array(state)
        evaluated = evaluationState * self.combinations
        score = sum(evaluated.flatten())
        
        return score

    
    
    def draw(self, window: pygame.Surface):
        for y, yList in enumerate(self.state):
            for x, val in enumerate(yList):
                if val == 0: continue
                
                windowPos = self.grid.getWindowPosFromGridPos(Vector2([x, y])) + Vector2([self.grid.cellSizePX//2]*2)
                pygame.draw.circle(window, self.texturePack[val], windowPos, self.grid.cellSizePX // 2 - 10)
    
    
    def __str__(self):
        return str(self.state)
    
    
    def print(self):
        for yList in self.state:
            print(yList)








class GhostShape:
    pos = Vector2(0, 0)
    
    def __init__(self, cellSizePX, initPlayer, texturePack):
        self.cellSizePX = cellSizePX * GHOST_SHAPE_SIZE_FACTOR
        self.color = "blue"
        self.player = initPlayer
        self.texturePack = texturePack
        
        
    def setPos(self, newPos: Vector2):
        self.pos = newPos
    
    def getRect(self):
        windowX = self.pos.x - self.cellSizePX // 2
        windowY = self.pos.y - self.cellSizePX // 2
        return pygame.Rect(windowX, windowY, self.cellSizePX, self.cellSizePX)
    
    def draw(self, window: pygame.Surface):
        pygame.draw.circle(window, self.texturePack[self.player], self.pos, self.cellSizePX * GHOST_SHAPE_SIZE_FACTOR / 2)



def generateCombinationMap(xCells, yCells, winLength):
    

    combinationsDiagonals: list[list[int]] = []
    
    maxDiagonalLength = min(xCells, yCells)
    maxLength = max(xCells, yCells)
    
    for y in range(yCells):
        yList = []
        
        for x in range(xCells):
            distX = min(x+1, xCells - x)
            distY = min(y+1, yCells - y)
            edgeDistance = min(distX, distY) # Distance from the current cell to the edge of the board
                
            possibleDiagonalLength = y + x + 1 if x + y + 1 < maxLength else maxLength - (x + y + 1 - maxDiagonalLength)
            possibleDiagonalLength -= winLength - 1
            possibleDiagonalLength = max(possibleDiagonalLength, 0)
            
            numCombinations = min(possibleDiagonalLength, edgeDistance, maxDiagonalLength, winLength)
            
            yList.append(numCombinations)
        
        mirrored = yList[::-1]
        yList = np.array(yList) + np.array(mirrored) # Take the sum of comniations for both diagonals
        
        combinationsDiagonals.append(yList)
    

    combinationsRows: list[list[int]] = []
    
    for y in range(yCells):
        numCombinations = []
        maxCominations = xCells - winLength + 1
        for x in range(xCells):
            distX = min(x+1, xCells - x)
            
            numCombinations.append(min(distX, maxCominations, winLength))
        combinationsRows.append(numCombinations)

    combinationsColumns: list[list[int]] = []
    
    for y in range(yCells):
        numCombinations = []
        maxCominations = yCells - winLength + 1
        for x in range(xCells):
            distY = min(y+1, yCells - y)
            
            numCombinations.append(min(distY, maxCominations, winLength))
        combinationsColumns.append(numCombinations)
    

    
    totalCombinations = np.array(combinationsDiagonals) + np.array(combinationsRows) + np.array(combinationsColumns)

    return totalCombinations


if __name__ == '__main__':
    
    startPlayer = -1
    
    state = [
        [ 1,  0,  0],
        [ 0, 0,  0],
        [ 0,  0,  0]
    ]
    
    xCells = 3
    yCells = 3
    
    winLength = 3
    depth = 10
    
    
    totalCombinations = generateCombinationMap(xCells, yCells, winLength)

    
    cellSize = 200 
            
    grid = Grid(0, 0, cellSize, xCells, yCells)
    board = Board(grid, None, 3, startPlayer, totalCombinations, state)
    
    # Depth at sizes that are fast enough
    # X, Y, WinLen: Depth
    # 3, 3, 3: Full
    # 3, 4, 3: Full-
    # 4, 4, 3: 8
    # 4, 5, 3: 6
    # 5, 5, 3: 5-6
    # 5, 6, 3: 5
    # 6, 6, 3: 4-5
    # 6, 7, 3: 4
    # 7, 7, 3: 4
    # 7, 8, 3: 4
    # 8, 8, 3: 3-4
    # 8, 9, 3: 3
    # 9, 9, 3: 3
    # 9, 10, 3: 3 (looong) 2 (shooort)
    # 10, 10, 3: 3 (looong) 2 (shooort)
    # 15, 15, 3: 2 (looong)
    # 20, 20, 3: 1 (long)
    # 100, 100, 3: 0 (looong)

    # board.print()
   
    # Let Minimax decide the first move
    
    
    bestAction = board.getBestAction(board.state, startPlayer)

    # bestValue = board.minimax(board.state, depth)
    
    # print(f"{bestValue}, ({bestAction.x}, {bestAction.y})")
    # winner = "Draw" if bestValue == 0 else "X" if bestValue > 0 else "O"
    # print(f"Best move: {bestAction}, Best Value: {bestValue}")