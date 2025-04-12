import pygame
from pygame.math import Vector2
from pygame.font import Font

import sys

from common.setup import FPS, BG_COLOR, CENTER
from .ui_elements import Button, Text



def startScreenLoop(window, clock):
    """
    Main loop for the start screen of the Snake game.
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock.
    Returns:
        bool: False when the start loop has ended.
    """
    
   
    # Initialize UI Elements
    titleText = Text(
        window,
        "Welcome!",
        font = Font(None, 100),
        color = "brown3",
        center = CENTER + Vector2(0, -200)
    )
    
    chooseText = Text(
        window,
        "Choose a Game to Play",
        font = Font(None, 40),
        color = "black",
        center = CENTER + Vector2(0, -75)
    )
    
    
    # Initialize Buttons
    buttonFont = Font(None, 36)
    buttonTextColor = "white"
    buttonColor = (0, 128, 255)
    buttonPadding = Vector2(20, 20)
    buttonBorderRadius = 10

    TTTButton = Button(window, "Tic Tac Toe", buttonFont, buttonColor, buttonTextColor, CENTER + Vector2(75, 0), buttonPadding, borderRadius=buttonBorderRadius)
    SnakeButton = Button(window, "Snake", buttonFont, buttonColor, buttonTextColor, CENTER + Vector2(-75, 0), buttonPadding, borderRadius=buttonBorderRadius)
    
    
    # Start Screen Loop    
    game = None
    gameChosen = False
    while not gameChosen:
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    if TTTButton.isPressed(event.pos):
                        game = "Tic Tac Toe"
                        gameChosen = True
                    elif SnakeButton.isPressed(event.pos):
                        game = "Snake"
                        gameChosen = True
                
                case pygame.KEYDOWN:
                    pass
                
                case _:
                    pass
        
        
        # Render Screen and all UI elements
        window.fill(BG_COLOR)

        TTTButton.draw()
        SnakeButton.draw()
        
        titleText.draw()
        chooseText.draw()
        
        # flip() to show changes
        pygame.display.flip()
    
    
        # Cap the frame rate to FPS
        clock.tick(FPS)

    # Return the chosen game
    return game