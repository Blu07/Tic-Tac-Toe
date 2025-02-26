from pprint import pprint
import numpy as np

class Board:
    
    
    r1 = np.array([-1, -1]) # Horizontal up left
    r2 = np.array([0, -1]) # Up
    r3 = np.array([1, -1]) # Horizontal up right
    r4 = np.array([1, 0]) # right
    
    dirVectors = [r1, r2, r3, r4]
    
    
    def __init__(self, size: int = 3, winLength: int = 3):
        
        self.size = size
        self.winLength = winLength
        
        # Initial board for testing
        self.board: list[list[int]] = [
            [1, 0, 0, -1],
            [1, 1, -1, 0],
            [0, -1, 0, 0],
            [0, -1, 1, 1],
        ]
    
    def addSpot(self, x: int, y: int, val = 0):
        """ Set the value in position (x, y) to val if the position is valid.
        Turns (x, y) coordinates [1, ->] to index values [0, ->].

        Args:
            x (int): The x coordinate to insert val. X-axis is horizontal, positive direction right.
            y (int): The y coordinate to insert val. Y-axis is vertical, positive direction down.
            val (int, optional): The value to insert at position (x, y). Defaults to 0.
        """
        
        if self.board[y - 1][x - 1] == 0:
            self.board[y - 1][x - 1] = val # Set the value at the correct index
            return True # Valid position, value successfully changed
        else: return False # Invalid position, value not changed.
    
    
    def getValAtPos(self, x, y):
        
        if x <= 0 or \
           x > self.size or \
           y <= 0 or \
           y > self.size:
               
            # x or y is out of the board
            return 0
        
        else:
            return self.board[y - 1][x - 1]
            
    
    
    def checkhasWon(self, x, y, val):
        
        for i, r in enumerate(self.dirVectors):
            # Use i to calculate if there is any possibility for the diagonals to be valid (i=0, i=2) in the corners.
            # Possible early return to save computation time over a small arithmetic calculation
            
            # print("new direction")
            checkX = x
            checkY = y
            
            inverted = False
            equal = True
            equalCount = 1 # The initial position has a valid value
            
            while equal:

                # print("r:", r)
                
                checkX += r[0]
                checkY += r[1]
                
                valAtCheck = self.getValAtPos(checkX, checkY)
                equal = valAtCheck == val
                # print("(", checkX, checkY, "):", valAtCheck, equal)
                
                if equal: equalCount += 1
                else:
                    if inverted: continue
                    
                    # Invert the searching direction and start searching form original position
                    # print("inverted search")
                    inverted = True
                    r *= -1
                    checkX = x
                    checkY = y
                    equal = True
                    
                if equalCount == self.winLength: return True # player has won
                
                # print("count:", equalCount)    

      
        
        # For-loop never found a winning case, so player did not win
        return False
        

    
    def __str__(self):
        return str(self.board)
    
    
    def print(self):
        for yList in self.board:
            print(yList)
    
    
        
board = Board(4, 4)

newPosX = 2
newPosY = 1
newVal = -1

board.print()
print(board.addSpot(newPosX, newPosY, newVal))

board.print()

print(board.checkhasWon(newPosX, newPosY, newVal))
