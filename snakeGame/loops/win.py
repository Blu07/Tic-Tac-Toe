import pygame
from pygame.math import Vector2
import sys

from snakeGame.ui_elements import Button, Text

from snakeGame.setup import FPS

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
    
    # Start Screen Setup
    BG_COLOR = "aquamarine"
    
    # Title Text
    TITLE = "You Won!"
    TITLE_COLOR = "brown3"
    TITLE_FONT = pygame.font.Font(None, 74)
    TITLE_CENTER = Vector2(window.get_width() // 2, 100)
    
    # Start Button
    RESTART_BUTTON_TEXT = "Click to Restart Game"
    RESTART_BUTTON_COLOR = (0, 128, 255)
    RESTART_BUTTON_TEXT_COLOR = (255, 255, 255)
    RESTART_BUTTON_FONT = pygame.font.Font(None, 24)
    RESTART_BUTTON_CENTER = Vector2(window.get_width() // 2, window.get_height() // 2)
    RESTART_BUTTON_PADDING = Vector2(50, 30)
    
    
    # Initialize UI Elements
    titleText = Text(window, TITLE_FONT, TITLE, TITLE_COLOR, center=TITLE_CENTER)
    restartButton = Button(window, RESTART_BUTTON_TEXT, RESTART_BUTTON_FONT, RESTART_BUTTON_COLOR, RESTART_BUTTON_TEXT_COLOR, center=RESTART_BUTTON_CENTER, padding=RESTART_BUTTON_PADDING)

    
    # Game Over Screen Loop
    while loop:
        
        events = pygame.event.get()
        
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    pass
                    mousePos = Vector2(pygame.mouse.get_pos())
                    if restartButton.pressed(mousePos):
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