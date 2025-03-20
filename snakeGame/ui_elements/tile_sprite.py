import pygame
from pygame.math import Vector2

from common.utils import vec2Deg


class TileSprite(pygame.sprite.Sprite):
    """A sprite representing a tile on the grid.
        The tile has a position and rotation, and a texture pack.
    """
    def __init__(self, grid, textures, style, pos: Vector2, rotation: int = 0):
        """Initializes the TileSprite.

        Args:
            grid (Grid): 
            textures (list): A list of textures for the tile.
            style (str): _description_
            pos (Vector2): _description_
            rotation (int, optional): _description_. Defaults to 0.

        Raises:
            ValueError: _description_
        """
        super().__init__()
        self.grid = grid
        self.pos = pos
        
        self.textures = textures
        self.style = style
        self.rotation = rotation

        # Get the top-left position on the screen from grid coordinates
        self.topleft = self.grid.getWindowPosFromGridPos(pos)

        # Get the texture for the current style
        self.texture = self.textures[self.style]
        if not self.texture:
            raise ValueError(f"Did not find texture for style: {self.style}")

        # Rotate the image if a rotation is specified
        if self.rotation:
            self.image = pygame.transform.rotate(self.texture, -self.rotation)  # Rotate counter-clockwise to match Pygame's clockwise rotation
        else:
            self.image = self.texture

        # Get the rect of the image
        self.rect = self.image.get_rect(topleft=self.topleft)


    def updatePos(self, pos):
        self.pos = pos
        self.topleft = self.grid.getScreenPosFromGridPos(pos)
        self.rect = self.image.get_rect(topleft=self.topleft)
    
    def updateStyle(self, style):
        self.style = style
        
        # Get the texture for the current style
        self.texture = self.textures[self.style]
        if not self.texture:
            raise ValueError(f"Did not find texture for style: {self.style}")

        # Rotate the image if a rotation is specified
        if self.rotation:
            self.image = pygame.transform.rotate(self.texture, -self.rotation)  # Rotate counter-clockwise to match Pygame's clockwise rotation
        else:
            self.image = self.texture

        # Get the rect of the image
        self.rect = self.image.get_rect(topleft=self.topleft)


    def update(self, *args, **kwargs):
        """Updates this tile. Takes in 'style', ('direction' or 'rotation') and/or 'pos' as keyword arguments.
        """
        
        style = kwargs.get("style")
        rotation = kwargs.get("rotation")
        direction = kwargs.get("direction")
        pos = kwargs.get("pos")
        
        if not rotation is None: self.rotation = rotation
        elif not direction is None: self.rotation = vec2Deg(direction)
        if not pos is None: self.updatePos(pos)
        if not style is None: self.updateStyle(style)
            
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    
    def __str__(self):
        return f"TileSprite({self.style}, {self.pos}, {self.rotation})"