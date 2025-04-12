import pygame

from common.setup import WINDOW_WIDTH, WINDOW_HEIGHT

from common.start import startScreenLoop

from snakeGame import mainSnakeLoop
from TicTacToeGame import mainTTTLoop

import os


os.environ['SDL_VIDEO_WINDOW_POS'] = '1' # Center the window on the screen

clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


# Start screen
pygame.display.set_caption("Select Game")

while True:
 
    game = startScreenLoop(window, clock)
    
    match game:
        case "Snake":
            mainSnakeLoop(window, clock)
            
        case "Tic Tac Toe":
            mainTTTLoop(window, clock)



pygame.quit()

