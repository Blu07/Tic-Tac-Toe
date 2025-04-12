import pygame
from pygame.math import Vector2
from pygame.font import Font
import sys

from common.ui_elements import Button, Text
from common.setup import FPS, CENTER

def gameOverLoop(window: pygame.Surface, clock: pygame.time.Clock, result: str) -> bool:
    """
    Game over loop that handles events and renders the game over screen.
    Parameters:
    - window (pygame.Surface): The game window surface.
    - loop (bool): Flag to control the loop.
    - clock (pygame.time.Clock): The game clock.
    Returns:
    - bool: False when the game over loop has ended.
    """
    
    title = "Game Over!" if result == "game_over" else "You Won!"
    

    # Initialize UI Elements
    titleText = Text(
        window,
        text = title,
        font = Font(None, 100),
        color = "blue",
        center = Vector2(CENTER.x, 100)
    )
    
    restartButton = Button(
        window,
        "Click to Restart Game",
        font = Font(None, 24),
        bgColor = (0, 128, 255),
        textColor="white",
        center = CENTER,
        padding = Vector2(20, 20),
        borderRadius = 10
    )

    
    # Game Over Screen Loop
    loop = True
    while loop:
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    if restartButton.isPressed(event.pos):
                        loop = False
                
                case pygame.KEYDOWN:
                    pass
                
                case _:
                    pass
        
        
        # Render Screen  
        restartButton.draw()
        titleText.draw()
        
        # flip() to show changes
        pygame.display.flip()
    
    
        # Cap the frame rate to FPS
        clock.tick(FPS)
