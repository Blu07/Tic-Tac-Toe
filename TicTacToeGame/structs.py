
import numpy as np
import pygame
from pygame import Vector2
from copy import deepcopy

from time import sleep

from .setup import SHAPE_SIZE_FACTOR, DEPTH, TEXTURE_PACK, AI_PERFORM_DELAY
from common.grid import Grid
from common.utils import loadTextures
from common.tileSprite import TileSprite

class Board:
    
    # Searching directions with relative vectors
    HUL = Vector2([-1, -1]) # Horizontal Up Left
    U = Vector2([0, -1]) # Up
    HUR = Vector2([1, -1]) # Horizontal Up Right
    R = Vector2([1, 0]) # Right
    
    dirVectors = [HUL, U, HUR, R]
    
    def __init__(self, grid: Grid, winLength: int = 3, startPlayer: int = 1, state = None):
        
        self.grid = grid 
        self.winLength = winLength
        self.startPlayer = startPlayer
                
        self.textures = loadTextures(
            texturePack=TEXTURE_PACK,
            size=grid.cellSizePX
        )
        
        # Initialize the board with all zeros with correct dimensions
        self.state = [ [0] * grid.numCellsX for _ in range(grid.numCellsY) ] if state is None else state
        
        self.tileSpriteList = []


    def checkHasWon(self, action: Vector2, player: int, state = None):
        """Check if the player has won the game by performing the action.
        This function checks for winning conditions only where the action is included.
        Args:
            action (Vector2): The position where the player has made their move.
            player (int): The player identifier (e.g., 1 or 2).
            state (optional): The current state of the game board. If not provided, the function will use the instance's state.
        Returns:
            bool: True if the player has won the game, False otherwise.
        """
        
        if state is None: state = self.state
        
        for i, r in enumerate(self.dirVectors):
            # TODO: Use i to calculate if there is any possibility for the diagonals to be valid (i=0, i=2) in the corners.
            # Possible early return to save computation time over a small arithmetic calculation
                     
            inverted = False # Flag to only invert once
            equal = True # Store if each checked cell has the same value as the player's value
            equalCount = 1 # The player has won if this count is the same as winlength
            
            checkPos = deepcopy(action)
            
            while equal:
                checkPos += r # Add the relative direction vector to the current position
                
                valueAtCheck = self.getValAtPos(checkPos, state)
                equal = valueAtCheck == player

                if equal: equalCount += 1
                else:
                    if inverted: continue
                    
                    # Invert the searching direction and start searching form original position
                    checkPos = deepcopy(action)
                    r *= -1
                    inverted = True
                    equal = True
                    
                if equalCount == self.winLength: return True # player has won
                      
        
        # For-loop never found a winning case, so player did not win
        return False
    
    
    def performAction(self, action: Vector2, player = 0) -> list[list[int]]:
        """ Perform an action on the board.
        Parameters:
        - action (Vector2): The position to add the player's value.
        - player (int): The player's value to add to the board.
        Returns:
        - bool: True if the action was successful, False otherwise.
        """
                
        success = False # Changes to true if the action was valid
        
        valueAtCell = self.getValAtPos(action, self.state)
        outOfBounds = self.grid.isOutOfBounds(action)
        
        if not outOfBounds and valueAtCell == 0:
            self.state[int(action.y)][int(action.x)] = player # Set the value at the correct index
            tileSprite = TileSprite(
                self.grid,
                self.textures,
                style = "X" if player == 1 else "O",
                pos = Vector2([action.x, action.y]),
                sizeFactor = SHAPE_SIZE_FACTOR
            )
            
            self.tileSpriteList.append(tileSprite)
            success = True
        
        return success # Return whether the action is valid
    
    
    
    def getActions(self, state = None) -> list[Vector2]:
        # Return a list of actions of Vector2([x, y]) pairs
        
        # TODO: If the board is symmetrical, only return actions that result in unique new states
        ## First case: board is empty
        
        # Symmetrical by mid of x axis and mid of y axis (x and y axes might not be equal length)
        
        # maxX = xCells // 2 + 1 (include middle column if xCells is odd)
        # maxY = yCells // 2 + 1 (include middle row)
        
        # TODO (or not): Sort the list of actions based on win conditions
            # If the player can win, return that action
            # If the opponent can win, return that action
            # If there is a blocking move, return that action
            # If there is a move that creates a fork, return that action
            # If there is a move where the opponent can create a fork, return that action
        
        
        
        
        
        
        if state is None: state = self.state
        
        actions = []
        for y, yList in enumerate(state):
            for x, val in enumerate(yList):
                action = Vector2(x, y)
                if val == 0:
                    actions.append(Vector2(action))
                
                # There is a value at the current position:
                # store the position and value
                
                
        
        # Sort the actions based on distance from any previous actions
        # Only sort if the board has more than 1 empty cell
        # sortedActions = []
        # distMap = distanceMap(state)
        
        # for i in range(1, max(np.array(distMap).flatten())+1):
        #     actionsOfI = []
        #     for y, row in enumerate(distMap):
        #         for x, val in enumerate(row):
        #             if val == 0: continue
                
        #             if val == i:
        #                 actionsOfI.append(Vector2([x, y]))
        
        
        #     sortedActions.extend(actionsOfI)

            
        # return sortedActions
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
    
    
    
    def result(self, state, action, playerVal):
        
        newState = deepcopy(state)
        newState[int(action.y)][int(action.x)] = playerVal
        return newState
        
    
          
    def minimax(self, state, player, depth=10, alpha=-np.inf, beta=np.inf, root=False):
        bestValue = -np.inf * player # The opposite of the player's goal
        bestAction = None
        
        actions = self.getActions(state)
        for action in actions:

            checkState = self.result(state, action, player)
                
            immidiateWin = self.checkHasWon(action, player, checkState)
            isDraw = self.isStateFull(checkState)
            
            # Checking:
            # 1. the player has won,
            # 2. the game is a draw,
            # 3. the depth is 0,
            # 4. the game is not over, continue the search
            if immidiateWin: bestValue, bestAction = player, action
            elif isDraw: bestValue, bestAction = 0, action
            elif depth == 0: bestValue, bestAction = self.evaluateState(checkState), action
            else:
                otherPlayer = -player
                newValue = self.minimax(state=checkState, player=otherPlayer, depth=depth-1, alpha=alpha, beta=beta)
                
                if player == 1 and newValue > bestValue:
                    bestValue = newValue
                    bestAction = action
                    alpha = max(alpha, newValue)
                    
                elif player == -1 and newValue < bestValue:
                    bestValue = newValue
                    bestAction = action
                    beta = min(beta, newValue)
                
                if beta <= alpha: break
            
            
        if root: return bestAction # Return the best action because minimax was called at the top level
        else: return bestValue # Return the value of the state because minimax was called at a lower level
            
    

    def evaluateState(self, state):
        # TODO: Go through each cell. Give the cell points for each line it is part of, but squared. 3 long line -> 3^2 = 9 points.
        
        evaluationState = np.array(state)
        evaluated = evaluationState * 2 # give points based on position on boarg.
        score = sum(evaluated.flatten())
        
        return score

    
    
    def draw(self, window: pygame.Surface):
        for tile in self.tileSpriteList:
            tile.draw(window)
                
    
    def __str__(self):
        return str(self.state)
    
    
    def print(self):
        for row in self.state:
            print(row)




        
def HumanPlayer(event, currentPlayer, grid: Grid, board: Board):
        
        action = grid.getGridPosFromWindowPos(Vector2(event.pos))
        
        validMove = board.performAction(action, currentPlayer)
        if not validMove: return False, False

        didWin = board.checkHasWon(action, currentPlayer)
        
        return validMove, didWin
        
        
    

def AIPlayer(board: Board, playerValue: int, lastMoveTime: int = 0):

    bestAction = board.minimax(board.state, playerValue, depth=DEPTH, root=True)
    if bestAction is None: return False, None
    
    currentTime = pygame.time.get_ticks()
    if currentTime - lastMoveTime < AI_PERFORM_DELAY:
        # Add a delay so that the time between each action made by an AI is at least AI_PERFORM_DELAY
        sleep((AI_PERFORM_DELAY - (currentTime - lastMoveTime))/1000)
        
    
    validMove = board.performAction(bestAction, playerValue)
    didWin = board.checkHasWon(bestAction, playerValue)
    
    return validMove, didWin


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
    # Testing what depth takes an acceptable time based on the size of the board and win length
    startPlayer = -1
    
    # state = [
    #     [ 1,  0,  0],
    #     [ 0, 0,  0],
    #     [ 0,  0,  0]
    # ]
    
    xCells = 3
    yCells = 3
    
    winLength = 3
    depth = 10
    
    
    totalCombinations = generateCombinationMap(xCells, yCells, winLength)

    
    cellSize = 200 
            
    grid = Grid(0, 0, cellSize, xCells, yCells)
    board = Board(grid, 3, startPlayer)
    
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
    
    
    bestAction = board.minimax(board.state, startPlayer, depth=depth, root=True)
    print(bestAction)
    
    # print(f"{bestValue}, ({bestAction.x}, {bestAction.y})")
    # winner = "Draw" if bestValue == 0 else "X" if bestValue > 0 else "O"
    # print(f"Best move: {bestAction}, Best Value: {bestValue}")