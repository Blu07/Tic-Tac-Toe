import pygame
from pygame.math import Vector2
import sys

from ..ui_elements import Button, Text
from TicTacToeGame.setup import FPS, GO_BG_COLOR, GO_TITLE, TEXTURE_PACK, GO_TITLE_COLOR, GO_TITLE_FONT, GO_RESTART_BUTTON_TEXT, GO_RESTART_BUTTON_FONT, GO_RESTART_BUTTON_COLOR, GO_RESTART_BUTTON_TEXT_COLOR, GO_RESTART_BUTTON_PADDING

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
    
    GO_TITLE_CENTER = Vector2(window.get_width() // 2, 100)
    GO_RESTART_BUTTON_CENTER = Vector2(window.get_width() // 2, window.get_height() // 2)

    if winner == 0: titleText = "It's a draw!"
    else: titleText = f"{TEXTURE_PACK[winner]} won!"

    
    # Initialize UI Elements
    titleText = Text(window, GO_TITLE_FONT, titleText, GO_TITLE_COLOR, center=GO_TITLE_CENTER)
    restartButton = Button(window, GO_RESTART_BUTTON_TEXT, GO_RESTART_BUTTON_FONT, GO_RESTART_BUTTON_COLOR, GO_RESTART_BUTTON_TEXT_COLOR, center=GO_RESTART_BUTTON_CENTER, padding=GO_RESTART_BUTTON_PADDING)

    
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
        
        # Fill the screen with the background color
        window.fill(GO_BG_COLOR)
        
        # Render Screen  
        restartButton.draw()
        titleText.draw()
        
        # flip() to show changes
        pygame.display.flip()
    
    
        # Cap the frame rate to FPS
        clock.tick(FPS)


    # Return False when startLoop has ended (pressed play etc.) 
    return False