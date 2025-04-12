import pygame
from pygame.math import Vector2
from pygame.font import Font
import sys

from common.ui_elements import Button, Text
from common.setup import CENTER, FPS

def gameOverLoop(window: pygame.Surface, loop: bool, clock: pygame.time.Clock, winner: str) -> bool:
    """
    Game over loop that handles events and renders the game over screen.
    Parameters:
    - window (pygame.Surface): The game window surface.
    - loop (bool): Flag to control the loop.
    - clock (pygame.time.Clock): The game clock.
    Returns:
    - bool: False when the game over loop has ended.
    """
    



    if winner == 0:
        title = "It's a draw!"
    else:
        player = "X" if winner == 1 else "O"
        title = f"{player} won!"
        
        
        
    pygame.display.set_caption(title)
    
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
        textColor = "white",
        center = CENTER,
        padding = Vector2(50, 30),
        borderRadius = 10
    )

    
    # Game Over Screen Loop
    while loop:
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit(),
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