import pygame
from pygame.math import Vector2
import sys
import numpy as np

from copy import deepcopy

from ..ui_elements import ScoreText
from TicTacToeGame.setup import FPS, GP_BACKGROUND_COLOR, DEPTH
from TicTacToeGame.structs import Grid, Board, GhostShape

def gameplayLoop(window: pygame.Surface, grid: Grid, board: Board, ghostShape: GhostShape, initPlayer: int, clock: pygame.time.Clock) -> bool:
    """
    Main gameplay loop for Tic Tac Toe.
    Args:
        window (pygame.Surface): The game window surface.
        loop (bool): Flag indicating whether the game loop should continue.
        clock (pygame.time.Clock): The game clock object.
    Returns:
        bool: False when gameplay has ended (e.g., when the snake crashes).
    """
    

    SCORE_FONT = pygame.font.Font(None, 34)
    scoreColor = "blue"
    scoreText = ScoreText(screen=window, font=SCORE_FONT, color=scoreColor)
    
    currentPlayer = initPlayer
    
    winner = None
    terminal = False
    
    


    while not terminal:
        
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminal = True
                pygame.quit()
                sys.exit()
                
            
            
            ## Player Input
            if currentPlayer == 1:
                if event.type == pygame.MOUSEMOTION:
                    # Update the position of the ghost shape to the mouse position
                    ghostShape.setPos(Vector2(event.pos))
                
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = grid.getGridPosFromWindowPos(Vector2(event.pos))
                    
                    validMove = board.performAction(action, currentPlayer) # No need to store the new state, as it is already stored in the board object
                    if not validMove: continue # Skip the rest because nothing should change

                    didWin = board.checkHasWon(action, currentPlayer)
                    
                    if didWin:
                        winner = currentPlayer
                        terminal = True
                    
    
                    
                    currentPlayer = -currentPlayer # Switch player between 1 and -1
                    ghostShape.player = currentPlayer
                    
                    break
            
            
            if currentPlayer == -1:
                    
                bestAction = board.minimax(board.state, -1, depth=DEPTH, root=True)

                # bestAction = board.getBestAction(board.state, -1, DEPTH)
                if bestAction is None:
                    winner = 0
                    terminal = True
                    break
                    
                board.performAction(bestAction, currentPlayer) # No need to know if the move was valid, as the AI always makes a valid move. State is already stored in the board object

                didWin = board.checkHasWon(bestAction, currentPlayer)
                
                if didWin:
                    winner = currentPlayer
                    terminal = True
                 
                
                currentPlayer = -currentPlayer # Switch player between 1 and -1
                ghostShape.player = currentPlayer

            
        # Render the screen with all elements, every frame.
        window.fill(GP_BACKGROUND_COLOR)

        scoreText.draw(3)
        
        grid.draw(window)
        board.draw(window)
        ghostShape.draw(window)

        pygame.display.flip()
        
        # Cap the frame rate to FPS
        clock.tick(FPS)
    
    # Return False when gameplay has ended (crashed etc.) 
    return winner
