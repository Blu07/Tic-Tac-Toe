import pygame
from pygame.math import Vector2
import os

from common.setup import TEXTURES_FOLDER

def getNextDirection(previousDir, event):
    """
    Determines the next direction based on the current direction and the keyboard input event.
    Parameters:
        currentDir (Vector2): The current direction as a 2D vector.
        event (pygame.event.Event): The keyboard input event.
    Returns:
        Vector2: The new direction as a 2D vector.
    """
    pass
    newDir = None
    
    # Directional constants as 2D Vector
    UP    = Vector2(0, -1)
    DOWN  = Vector2(0, 1)
    LEFT  = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    
    # Keyboard Input
    upKeys    = (pygame.K_UP, pygame.K_w)
    downKeys  = (pygame.K_DOWN, pygame.K_s)
    leftKeys  = (pygame.K_LEFT, pygame.K_a)
    rightKeys = (pygame.K_RIGHT, pygame.K_d)
    
    # Determine new direction
    newDir = (
             UP    if event.key in upKeys    and previousDir != DOWN
        else DOWN  if event.key in downKeys  and previousDir != UP
        else LEFT  if event.key in leftKeys  and previousDir != RIGHT
        else RIGHT if event.key in rightKeys and previousDir != LEFT
        else previousDir  # No change if movement is invalid (i.e. opposite current direction)
    )
    
    return newDir


def pos2IntXY(vector: Vector2):
    """
    Converts a Vector2 object to integer x and y coordinates.

    Parameters:
        vector (Vector2): The Vector2 object to convert.

    Returns:
        tuple: A tuple containing the integer x and y coordinates.
    """
    return int(vector.x), int(vector.y)


def vec2Deg(vector: Vector2) -> int:
    """Converts a 2D vector into an angle in degrees relative to the positive y-axis (up direction).

    Parameters:
        vector (Vector2): A 2D vector representing a direction.

    Returns:
        int: The angle in degrees (0-360) relative to the positive y-axis.
    """
    
    UP    = Vector2(0, -1)
    DOWN  = Vector2(0, 1)
    LEFT  = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    
    if vector == UP:
        return 0
    if vector == RIGHT:
        return 90
    if vector == DOWN:
        return 180
    if vector == LEFT:
        return 270


def deg2Vec(rotation: int) -> Vector2:
    """Converts an angle in degrees, relative to the positive y-axis (up direction), into a 2D vector.

    Parameters:
        rotation (int): An Integer representing a rotation.

    Returns:
        direction (Vector2): The 2D vector representing a screen direction.
    """
    
    UP    = Vector2(0, -1)
    DOWN  = Vector2(0, 1)
    LEFT  = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    
    if rotation == 0:
        return UP
    if rotation == 90:
        return RIGHT
    if rotation == 180:
        return DOWN
    if rotation == 270:
        return LEFT

def dir2Vec(direction: str) -> Vector2:
    """Converts a direction string into a 2D vector.

    Parameters:
        direction (str): A string representing a direction (e.g., "up", "down", "left", "right").

    Returns:
        Vector2: The corresponding 2D vector.
    """
    
    UP    = Vector2(0, -1)
    DOWN  = Vector2(0, 1)
    LEFT  = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    
    if direction == "up":
        return UP
    if direction == "down":
        return DOWN
    if direction == "left":
        return LEFT
    if direction == "right":
        return RIGHT

def getRelativeTurn(dir1: Vector2, dir2: Vector2):
    
    if (dir2.x * dir1.y) - (dir2.y * dir1.x) > 0:
        return "left"
    elif (dir2.x * dir1.y) - (dir2.y * dir1.x) < 0:
        return "right"
    elif dir2 == dir1:
        return "forward"
    elif dir1 == -dir2:
        return "backward"
    else:
        return "Unknown"
    

def loadTexture(file_name: str, size=None) -> pygame.Surface | None:
    """Load an image file and optionally resize it.

    Parameters:
        file_name (str): The path to the image file.
        size (tuple, optional): The desired size of the image. Defaults to None.

    Returns:
        pygame.Surface: The loaded and optionally resized image texture, or None if failed to load.

    """
    try:
        texture = pygame.image.load(os.path.join(TEXTURES_FOLDER, file_name)).convert_alpha()
        if size:
            if isinstance(size, int):
                size = (size, size)
            texture = pygame.transform.scale(texture, size)
        
        return texture
    except pygame.error as e:
        print(f"Failed to load texture {file_name}: {e}")
        return None


def loadTextures(size: tuple[int, int], texturePack: str, fileNames: list = None) -> dict:
    """Load textures based on a list of file names and a size.

    Parameters:
        fileNames (list[str]): A list of file names for the textures.
        size (tuple[int, int]): The desired size of the textures.

    Returns:
        dict: A dictionary containing the loaded textures.
            The keys are the names of the textures (extracted from the file names) and the values are the loaded textures.
    """
    textures = {}
    pathNames = []
    
    if fileNames: 
        pathNames = [os.path.join(texturePack, fileName) for fileName in fileNames]
    
    else:
        pathNames = [os.path.join(texturePack, fileName) for fileName in os.listdir(os.path.join(TEXTURES_FOLDER, texturePack))]
        
    for pathName in pathNames:
        texture = loadTexture(pathName, size)
        if texture:
            textureName = pathName.split('/')[-1].split('.')[0]  # Extract texture name from file name
            textures[textureName] = texture
            
    return textures



def isOutOfBounds(pos: Vector2, xLen, yLen):
    """Check if a given cell is out of bounds based on the size of the map
    """
    
    return pos.x < 0 or pos.x >= xLen or pos.y < 0 or pos.y >= yLen


def distanceMap(map: list[list[int]]):
    """Create a distance map from a 2D array of cells. The distance map contains the distance from each cell to the nearest
    obstacle cell.

    Args:
        map (list[list[int]]): A 2D array of cells with integer values 0 or 1. 0 is an open cell, any other value is an obstacle cell.

    Returns:
        list[list[int]]: A 2D array of cells with integer values representing the distance from each cell to the nearest obstacle cell.
    """

    # Create a new map with the same size as the input map, initialized with infinity. The algortihm chooses lower values
    # for the cells, so infinity will always be replaced.
    distMap = [[float('inf') for _ in range(len(map[0]))] for _ in range(len(map))]
    # All 8 neighbors as relative coordinates
    neighborsDXDY = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]
    
    # first, set the distance to 0 for all cells that are obstacles
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] != 0:
                distMap[y][x] = 0
    
    i = 0
    
    # Algorithm:
    # then, loop through the distMap and set the distance to i+1 for all neighbors of the each cell with value i
    # increment i by 1 and repeat until no changed were made.
    
    changed = True
    while changed:
        
        changed = False
        
        # Loop through all cells for the current i
        for y in range(len(distMap)):
            for x in range(len(distMap[0])):

                # skip all cells that are not i
                if distMap[y][x] != i: continue
                
                # loop through all neighbors of i-cells
                for dy, dx in neighborsDXDY:
                    X, Y = x+dx, y+dy
                    
                    # skip invalid positions
                    if isOutOfBounds(Vector2(X, Y), len(map[0]), len(map)): continue
                    
                    # Set the value of the neighbor cell to i+1 if the current value is greater than i+1
                    if distMap[Y][X] > i+1:
                        distMap[Y][X] = i+1
                        changed = True
    
        # Continue while-loop with the next i
        i += 1
    
    return distMap

            
    