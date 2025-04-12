import pygame
from pygame.math import Vector2
import sys

from common.ui_elements import Button, Text
from common.setup import FPS, CENTER


def winLoop(window: pygame.Surface, loop: bool, clock: pygame.time.Clock) -> bool:
    """
    Game over loop that handles events and renders the game over screen.
    Parameters:
    - window (pygame.Surface): The game window surface.
    - loop (bool): Flag to control the loop.
    - clock (pygame.time.Clock): The game clock.
    Returns:
    - bool: False when the game over loop has ended.
    """
    
    
    # Initialize UI Elements
    titleText = Text(
        window,
        "You Won!",
        font = pygame.font.Font(None, 74),
        color = "brown3",
        center = CENTER + Vector2(0, -200)
    )
    
    restartButton = Button(
        window,
        "Click to Restart Game",
        font = pygame.font.Font(None, 24),
        bgColor = (0, 128, 255),
        textColor = "white",
        center = CENTER,
        padding = Vector2(50, 30)
    )

    
    # Game Over Screen Loop
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


    # Return False when startLoop has ended (pressed play etc.) 
    return False