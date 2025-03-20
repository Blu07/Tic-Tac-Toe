from pprint import pprint
import numpy as np
import pygame
from pygame import Vector2
from copy import copy, deepcopy

from .setup import GHOST_SHAPE_SIZE_FACTOR, DEPTH
from common.grid import Grid


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
        

            
        success = False # Change to true if the action was successful
        
        valueAtCell = self.getValAtPos(action, self.state)
        outOfBounds = self.grid.isOutOfBounds(action)
        
        if not outOfBounds and valueAtCell == 0:
            self.state[int(action.y)][int(action.x)] = player # Set the value at the correct index
            success = True
        
        return success # Return whether the action was successful or not
    
    
    
    def getActions(self, state = None) -> list[Vector2]:
        # Return a list of actions of Vector2([x, y]) pairs
        
        # TODO: If the board is symmetrical, only return actions that result in unique new states
        ## First case: board is empty
        
        # Symmetrical by mid of x axis and mid of y axis (x and y axes might not be equal length)
        
        # maxX = xCells // 2 + 1 (include middle column if xCells is odd)
        # maxY = yCells // 2 + 1 (include middle row)
        
        # TODO: Sort the list of actions based on win conditions
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
    
          
    def minimax(self, state, player, depth=10, alpha=-np.inf, beta=np.inf, root=False):
        bestValue = -np.inf * player # The opposite of the player's goal
        bestAction = None
        
        actions = self.getActions(state)
        for action in actions:

            checkState = self.Result(state, action, player)
                
            immidiateWin = self.checkHasWon(action, player, checkState)
            isDraw = self.isStateFull(checkState)
            
            # Check:
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
            
    
    def getBestAction(self, state, player, depth=10):        
        state = deepcopy(state)
        
        bestAction = self.minimax(state, player, depth=depth, root=True)
        print(bestAction)
        return bestAction

        # bestValue = -player * np.inf  # Opposite of player's goal
        # bestAction = None
        # bestActions = []
        
        # values = []
        
        # otherPlayer = -player

        # actions = self.getActions(state)
        # for action in actions:
        #     newState = self.Result(state, action, player)
            
        #     if self.checkHasWon(action, player, newState): return action
        #     if self.isStateFull(newState): return action
            
        #     value, bestActions = self.minimax(newState, otherPlayer, depth=depth)
        #     print(bestActions)
        #     if player == 1:     bestValue = max(bestValue, value)
        #     elif player == -1:  bestValue = min(bestValue, value)
            
        #     values.append(value)

        #     bestAction = actions[values.index(bestValue)]
        
        
        # return bestAction




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
    board = Board(grid, None, 3, startPlayer, totalCombinations)
    
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