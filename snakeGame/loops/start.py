import pygame
from pygame.math import Vector2
import sys

from snakeGame.ui_elements import Button, Text
from snakeGame.setup import FPS, S_TITLE, S_TITLE_COLOR, S_TITLE_FONT, S_BG_COLOR, S_START_BUTTON_TEXT, S_START_BUTTON_FONT, S_START_BUTTON_COLOR, S_START_BUTTON_TEXT_COLOR, S_START_BUTTON_PADDING

def startScreenLoop(window, loop, clock):
    """
    Main loop for the start screen of the Snake game.
    Args:
        window (pygame.Surface): The game window surface.
        loop (bool): Flag to control the loop.
        clock (pygame.time.Clock): The game clock.
        FPS (int): The desired frame rate.
    Returns:
        bool: False when the start loop has ended.
    """
    
    
    S_TITLE_CENTER = Vector2(window.get_width() // 2, 100)
    S_START_BUTTON_CENTER = Vector2(window.get_width() // 2, window.get_height() // 2)

   
    # Initialize UI Elements
    titleText = Text(window, S_TITLE_FONT, S_TITLE, S_TITLE_COLOR, center=S_TITLE_CENTER)
    startButton = Button(window, S_START_BUTTON_TEXT, S_START_BUTTON_FONT, S_START_BUTTON_COLOR, S_START_BUTTON_TEXT_COLOR, center=S_START_BUTTON_CENTER, padding=S_START_BUTTON_PADDING)
    
    # Start Screen Loop    
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
                    if startButton.pressed(mousePos):
                        loop = False
                
                case pygame.KEYDOWN:
                    pass
                
                case _:
                    pass
        
        
        # Render Screen and all UI elements
        window.fill(S_BG_COLOR)

        startButton.draw()
        titleText.draw()
        
        # flip() to show changes
        pygame.display.flip()
    
    
        
        # Cap the frame rate to FPS
        clock.tick(FPS)


    # Return False when startLoop has ended (pressed play etc.) 
    return False