import pygame
from pygame import Vector2
import random
import os

from common.setup import TEXTURES_FOLDER
from common.grid import Grid

from snakeGame.ui_elements import TileSprite
from common.utils import pos2IntXY, loadTextures, getRelativeTurn, vec2Deg
from snakeGame.setup import RANDOM_FOOD_MAX_ATTEMPTS, SNAKE_TEXTURE_PACK, FOOD_TEXTURE_PACK, HOTSPOT_TEXTURE_PACK

class Food(): ...
class HotSpots(): ...
class Snake(): ...


class FoodList():
    def __init__(self, screen: pygame.Surface, grid: Grid):
        """
        Initializes a FoodList object.
        Args:
            screen: The screen object where the food will be displayed.
            grid: The grid object representing the game grid.
        """

        self.screen = screen
        self.grid = grid

        self.foodList: list = []  # One list to keep track of all the food items
        self.foodArray: list = [[None for _ in range(grid.numCellsX)] for _ in range(
            grid.numCellsY)]  # One grid to keep track of food items at each cell

        # Load textures on Init
        cellSize = (grid.cellSizePX, grid.cellSizePX)
        self.textures = loadTextures(
            texturePack=FOOD_TEXTURE_PACK, size=cellSize)

    def isFoodAtPos(self, pos: Vector2) -> bool:
        """Checks if there is a food item at the given position.

        Args:
            pos (Vector2): The position to check.

        Returns:
            bool: True if there is a food item at the position, False otherwise.
        """

        x, y = pos2IntXY(pos)
        
        outOfBounds = self.grid.isOutOfBounds(pos)
        if outOfBounds:
            return False
        
        if isinstance(self.foodArray[y][x], TileSprite):
            return True

        return False


    def addFood(self, food: TileSprite):
        """
        Adds a food tile to the food list and updates the foodArray grid.
        Parameters:
            food (TileSprite): The food tile to be added.
        """
        x = int(food.pos.x)
        y = int(food.pos.y)

        self.foodArray[y][x] = food
        self.foodList.append(food)


    def removeFood(self, food: TileSprite):
        """
        Removes the specified food from the food list and updates the food tiles grid.
        Parameters:
            food (TileSprite): The food to be removed.
        """
        x, y = pos2IntXY(food.pos)

        self.foodList.remove(food)
        self.foodArray[y][x] = None


    def removeAtPos(self, pos: Vector2):
        """
        Removes the food at the specified position from the food list and updates the food tiles grid.
        Args:
            pos (Vector2): The position of the food to be removed.
        """
        x, y = pos2IntXY(pos)
        food = self.foodArray[y][x]

        self.foodList.remove(food)
        self.foodArray[y][x] = None


    def newRandomFood(self, snake: Snake, hotSpotList: HotSpots, invalidPositions = []) -> bool:
        """
        Generates a new random food item on the grid that is not already occupied by the snake.
        Parameters:
            snake: The snake object representing the player's snake.
            hotSpotList: The HotSpotList object containing the hotspots in the game.
            invalidPositions: An extra list of positions that are invalid for placing food.
        Returns:
            bool: True if the food was successfully placed, False otherwise.
        """

        # Find all the valid tiles where food can be placed
        validTiles = []
        for y in range(self.grid.numCellsY):
            for x in range(self.grid.numCellsX):
                pos = Vector2(x, y)
                isSnakePos = snake.posAlreadyInSnake(pos)
                isHotSpotPos = hotSpotList.isHotSpotAtPos(pos)
                isFoodPos = self.isFoodAtPos(pos)
                isInvalid = pos in invalidPositions
                
                if not isSnakePos and not isHotSpotPos and not isFoodPos and not isInvalid:
                    validTiles.append(pos)
        
        if not validTiles:
            # This can happen if the grid is filled with either snake, hotspots or food
            # current implementation is that the player wins now
            return False
        
        # Randomly select a food texture from the texture pack and create a new food tile at a random position
        foodType = random.choice(os.listdir(os.path.join(TEXTURES_FOLDER, FOOD_TEXTURE_PACK))).split('.')[0]
        pos = random.choice(validTiles)
        newFood = TileSprite(grid=self.grid, pos=pos, textures=self.textures, style=foodType, rotation=0)
        self.addFood(newFood)
        
        return True
    

    

    def draw(self):
        """
        Draws all the food items in the food list on the screen.

        Parameters:
            self: The FoodList object.
        """
        for food in self.foodList:
            food.draw(self.screen)


class HotSpotList():
    def __init__(self, screen, grid: Grid, threshold: int = 5):
        """
        Initializes a SnakeGame object.
        Args:
            screen: The screen object where the game will be displayed.
            grid: The grid object representing the game grid.
            threshold: The threshold value for the hotspots.
        """
        self.screen = screen
        self.grid = grid
        
        self.threshold = threshold
        
        self.hotSpotArray = [[0 for _ in range(grid.numCellsX)] for _ in range(grid.numCellsY)]
        self.hotSpotList = []
        
        gridSize = Vector2(grid.cellSizePX, grid.cellSizePX)
        self.textures = loadTextures(texturePack=HOTSPOT_TEXTURE_PACK, size=gridSize)
    
    
    def increaseLevelAtPos(self, pos: Vector2):
        """
        Increases the level at the given position in the hotSpots grid.
        
        A cell in the HotSpot grid goes through the following states:
            - int: The level of the hotspot (0 to threshold)
            - TileSprite: The hotspot is empty (no hotspot, but used as a transition fro int to hotspot)
            - TileSprite: The hotspot is cracked
            - TileSprite: The hotspot is a hotspot
        
        Args:
            pos (Vector2): The position in the grid to increase the level at.
        """
        x, y = pos2IntXY(pos)
        cell = self.getCellAtPos(pos)
        
        # Integer counter
        if isinstance(cell, int):
            # If the value is an integer, variable cell is not a reference to the cell in the array, so we need to update the array directly.
            self.hotSpotArray[y][x] += 1
            
            if cell == self.threshold:
                self.turnPosIntoSprite(pos, style="empty")
            
        # Hot spot states
        elif isinstance(cell, TileSprite):
            if cell.style == "empty":
                self.turnPosIntoSprite(pos, style="crack")
        
            elif cell.style == "crack":
                self.turnPosIntoSprite(pos, style="hotspot")
                
        else:
            print(f"Failed to increase level of cell {cell} at {pos}")
        
    
    def turnPosIntoSprite(self, pos: Vector2, style: str):
        """
        Turns the given position into a hot spot on the grid.
        Args:
            pos (Vector2): The position to be turned into a hot spot.
        """
        x, y = pos2IntXY(pos)
        hotSpot = TileSprite(grid=self.grid, textures=self.textures, style=style, pos=pos, rotation=0)
        
        self.hotSpotArray[y][x] = hotSpot
        self.hotSpotList.append(hotSpot)
        
        
    def turnSpriteIntoPos(self, pos: Vector2):
        """
        Turns the hot spot at the given position into a regular position.
        Args:
            pos (Vector2): The position of the hot spot to be turned into a regular position.
        """
        x, y = pos2IntXY(pos)
        hotSpot = self.hotSpotArray[y][x]
        
        self.hotSpotArray[y][x] = 0
        self.hotSpotList.remove(hotSpot)
    
        
    def isHotSpotAtPos(self, pos: Vector2, includeCrack = False) -> bool:
        """
        Check if there is an active hotSpot at the given position.
        Args:
            pos (Vector2): The position to check.
        Returns:
            bool: True if there is a hot spot at the given position, False otherwise.
        """
        
        isOutOfBounds = self.grid.isOutOfBounds(pos)
        # Do not check array if position is out of bounds (list index out of range)
        if isOutOfBounds:
            return False
        
        tile = self.getCellAtPos(pos)
        if isinstance(tile, TileSprite):
            if tile.style == "hotspot":
                return True
            elif includeCrack and tile.style == "crack":
                return True
        
        # Cell is not hotspot
        return False


    def getCellAtPos(self, pos: Vector2):
        """
        Returns the cell at the given position.

        Args:
            pos (Vector2): The position of the cell.

        Returns:
            The cell at the given position.
        """
        x, y = pos2IntXY(pos)
        return self.hotSpotArray[y][x]


    def draw(self):
        """
        Draws the hot spots on the screen.

        Parameters:
            self: The instance of the class.
        """
        for hotSpot in self.hotSpotList:
            hotSpot.draw(self.screen)


class Snake():
    def __init__(self, screen, grid: Grid, foodList: FoodList, hotSpotList: HotSpotList, startX: int = 2, startY: int = 2, startLen: int = 3, initDirection: Vector2 = Vector2(1, 0), color: str = "blue", pointsPerFood: int = 1):
        """
        Initializes a Snake object.
        Parameters:
            screen: The screen object where the snake will be displayed.
            grid: The grid object representing the game grid.
            foodList: The list of food objects in the game.
            hotSpotList: The list of hot spot objects in the game.
            startX: The starting x-coordinate of the snake's head.
            startY: The starting y-coordinate of the snake's head.
            startLen: The starting length of the snake.
            initDirection: The initial direction of the snake.
            color: The color of the snake.
            pointsPerFood: The number of points the snake earns per food eaten.
        """
        
        
        # Game Related
        self.screen = screen
        self.grid = grid
        self.foodList = foodList
        self.hotSpotList = hotSpotList
        
        self.pos = Vector2(startX, startY)
        
        # Load textures on Init
        cellSize = (grid.cellSizePX, grid.cellSizePX)
        self.textures = loadTextures(texturePack=SNAKE_TEXTURE_PACK, size=cellSize)
        
        # Snake Related
        self.len = startLen
        self.direction = initDirection
        self.color = color
        self.score = startLen
        self.pointsPerFood = pointsPerFood
        
        # 2D array to store the snake tiles at each cell, usefull for quickly checking if a position is occupied by a snake tile
        # The snakeArray includes a border around the grid, so add 2 cells in each x and y directions
        self.snakeArray: list = [[None for _ in range(grid.numCellsX + 2)] for _ in range(grid.numCellsY + 2)]
        
        
        # Initialize snake with head tile
        # Generate snake with length of startLen
        # Add snakeTiles from the back of the snake, and forward: Snake.addSnakeTile() works this way
        self.snakeList: list = []
        for i in range(startLen-1, 0, -1):
            pos = self.pos - self.direction*i        
            self.addSnakeTile(pos, direction=self.direction, style="straight")
            
        # The head
        self.addSnakeTile(self.pos, direction=self.direction, style="head")
    
    
    def addSnakeTile(self, pos, direction=Vector2(0, 1), style="head"): # style is default "head" because adding a new snake tile is most often the new head
        """
        Adds a new snake tile to the snake list and updates the snakeArray grid.

        Parameters:
            pos: The position of the new snake tile.
            direction: The direction of the new snake tile. Default is Vector2(0, 1).
            style: The style of the new snake tile. Default is "head".

        Returns:
            None
        """
        
        rotation = vec2Deg(direction)
        snakeTile = TileSprite(grid=self.grid, pos=pos, textures=self.textures, rotation=rotation, style=style)
        self.snakeList.insert(0, snakeTile)
        self.snakeArray[int(pos.y) + 1][int(pos.x) + 1] = snakeTile # The snakeArray includes a border around the grid, so add 1 to x and y
    
    
    def posAlreadyInSnake(self, pos) -> bool:
        """
        Checks if a given position is already occupied by a snake tile.
        Parameters:
            pos: The position to check.
        Returns:
            bool: True if the position is already occupied by a snake tile, False otherwise.

        """
        
        if isinstance(self.getTileAtPos(pos), TileSprite):
            return True

        return False
    
    
    def getTileAtPos(self, pos: Vector2) -> TileSprite | None:
        """Return the snakeTile at the given position in the snakeArray grid.

        Args:
            pos (Vector2): the position to check in the snakeArray.

        Returns:
            (TileSprite | None): The snakeTile at the given position, or None if the snake is not at the position.
        """
        
        
        # The snakeArray includes a border around the grid, so add 1 to x and y to represent the actual grid position
        # Also, there is not need to check if it is out of bounds, because the grid is already padded with a border
        x, y = pos2IntXY(pos)
        x += 1
        y += 1
        
        # Do not check if the position is out of bounds, because
        return self.snakeArray[y][x]
    
    
    def setTileAtPos(self, pos: Vector2, tile: TileSprite | None):
        """
        Set the snakeTile at the given position in the snakeArray grid.

        Args:
            pos (Vector2): The position to set in the snakeArray.
            tile (TileSprite | None): The snakeTile to set at the given position.
        """
        
        x, y = pos2IntXY(pos)
        x += 1
        y += 1
        
        self.snakeArray[y][x] = tile
    
    
    def move(self, nextDirection: Vector2 = None, previousWasGraceMove: bool = False):
        """
        Moves the snake in the specified direction and updates its position on the grid.
        
        Args:
            nextDirection (Vector2, optional): The direction in which the snake should move. Defaults to None.
            wasGraceMove (bool, optional): Indicates if the previous move was a grace move. Defaults to False.
        Returns:
            died (bool): True if the snake died, False otherwise.
            doMove (bool): True if the snake moved, False otherwise.
        """
        
        
        isOpenMove = True
        died = False
        won = False
        
        didEat = False
        
        isOutOfBounds = False
        isSnakePos = False
        isHotSpotPos = False
        
        currentHead: TileSprite = self.snakeList[0]
        currentTail: TileSprite = self.snakeList[-1]
        relativeTurn = getRelativeTurn(self.direction, nextDirection) # How the snake tile of the current head should look after the move.
        
        
        # Set style to the texture type based on direction change.
        if relativeTurn == "left" or relativeTurn == "right":
            headNewStyle = relativeTurn
            self.direction = nextDirection
            
            # If the player turns into an obstacle, they should die right away because it was their "choice".
            # By setting previousWasGraceMove to True, the algorithm lets the player move into the obstacle right away without giving them another grace move. 
            previousWasGraceMove = True
            
        elif relativeTurn == "forward" or relativeTurn == "backward":
            headNewStyle = "straight"
            self.direction = self.direction
        
        
        # if not nextDirection == self.direction:
        #     # The player 
        #     previousWasGraceMove = True
      
      
        nextPos = currentHead.pos + self.direction
      
                
        # Check what the next position is occupied by (if anything)
        isOutOfBounds = self.grid.isOutOfBounds(nextPos)
        isSnakePos = self.posAlreadyInSnake(nextPos) and self.getTileAtPos(nextPos).style != "tail" # Exclude the tail, because it will move
        isHotSpotPos = self.hotSpotList.isHotSpotAtPos(nextPos)
        isFoodPos = self.foodList.isFoodAtPos(nextPos)

        # If there is food, eat it.
        if isFoodPos:
            didEat = True
            self.foodList.removeAtPos(nextPos)
            for _ in range(50):
                won = not self.foodList.newRandomFood(self, self.hotSpotList, invalidPositions=[nextPos])
            self.score += self.pointsPerFood


        
        isOpenMove: bool = not (isOutOfBounds or isSnakePos or isHotSpotPos) # Whether the next position is occupied or not.
        doMove: bool = isOpenMove or previousWasGraceMove # If the previous move was a grace move, the snake should move even if the next position is occupied.
        died: bool = doMove and not isOpenMove
        
        if doMove:
            # Update which is the tail 
            # Increase the level of the hotspot at the current tail position
            # Add a new snake tile at the next position
            
            if not didEat:
                # Remove the tail if the snake did not eat
                self.snakeList.pop()
                self.setTileAtPos(currentTail.pos, None)
            
            # Tail
            newTail: TileSprite = self.snakeList[-1]
            secondLastTail: TileSprite = self.snakeList[-2]
            newTail.update(style="tail", rotation=secondLastTail.rotation)
            
            # Head
            currentHead.update(style=headNewStyle)
            self.addSnakeTile(nextPos, self.direction, style="head")
            
            # Hot Spot
            self.hotSpotList.increaseLevelAtPos(currentTail.pos)
        
        # Return the boolean value that determines if the game should continue (died) and whether or not the snake moved (doMove; for grace move logic)
        return died, doMove, won
        


    def draw(self) -> None:
        """
        Draw the snake on the screen.

        Parameters:
            self: The Snake object.

        """
        for thisTile in self.snakeList:
            thisTile.draw(self.screen)

