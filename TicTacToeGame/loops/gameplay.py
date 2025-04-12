import pygame
from pygame.math import Vector2
import sys

from common.ui_elements import Text
from common.setup import FPS, GAMEPLAY_BG_COLOR

from TicTacToeGame.setup import HUMAN_THINKING_TEXT, AI_THINKING_TEXT
from TicTacToeGame.structs import Grid, Board, AIPlayer, HumanPlayer


    

def gameplayLoop(window: pygame.Surface, grid: Grid, board: Board, initPlayer: int, players, clock: pygame.time.Clock) -> bool:
    """
    Main gameplay loop for Tic Tac Toe.
    Args:
        window (pygame.Surface): The game window surface.
        loop (bool): Flag indicating whether the game loop should continue.
        clock (pygame.time.Clock): The game clock object.
    Returns:
        bool: False when gameplay has ended (e.g., when the snake crashes).
    """
    
    
    currentPlayer = initPlayer
    
    currentPlayerText = Text(
        window,
        text = f"Current Player: {"X" if currentPlayer == 1 else "O"}",
        font = pygame.font.Font(None, 60),
        color = "black",
        center = Vector2(window.get_width() // 2, 100)
    )
    
    currentPlayerDescription = Text(
        window,
        text = HUMAN_THINKING_TEXT if players[currentPlayer] == "Human" else AI_THINKING_TEXT,
        font = pygame.font.Font(None, 24),
        color = "black",
        center = Vector2(window.get_width() // 2, 140)
    )
    
    AICooldownFrames = 5 # Hard wait for AI to start. Used to ensure screen draws before AI starts thinking 
    
    winner = None
    terminal = False

    lastAIMoveTime = 0

    while not terminal:

        AICooldownFrames -= 1
        
        currentPlayerType = players[currentPlayer]
        validMove = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminal = True
                pygame.quit()
                sys.exit()
            
            # Player is human and made a move by clicking
            if currentPlayerType == "Human" and event.type == pygame.MOUSEBUTTONDOWN:
                validMove, didWin = HumanPlayer(event, currentPlayer, grid, board)
                
        
        # Player is AI and should make a move regardless of the event  
        if currentPlayerType == "AI" and AICooldownFrames <= 0:
            validMove, didWin = AIPlayer(board, currentPlayer, lastMoveTime=lastAIMoveTime)
            lastAIMoveTime = pygame.time.get_ticks()
            AICooldownFrames = 5 # Reset
            
        
        # If a valid move was made this frame, check for win or draw
        if validMove:
            # Draw
            if board.isStateFull():
                terminal = True
                winner = 0

            # Win
            elif didWin:
                winner = currentPlayer
                terminal = True
            
            # Nothing, continue game
            else:
                # Switch player between 1 and -1
                currentPlayer = -currentPlayer
                currentPlayerText.updateText(f"Current Player: {"X" if currentPlayer == 1 else "O"}")
                currentPlayerDescription.updateText(HUMAN_THINKING_TEXT if players[currentPlayer] == "Human" else AI_THINKING_TEXT)
                
        
                
        # Render the screen before processing events, so that
        window.fill(GAMEPLAY_BG_COLOR)

        currentPlayerText.draw()
        currentPlayerDescription.draw()
        
        grid.draw(window)
        board.draw(window)

        pygame.display.flip()

        
        # Cap the frame rate to FPS
        clock.tick(FPS)
    
    
    return winner
