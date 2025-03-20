import pygame
from pygame.math import Vector2
import sys
import numpy as np

from common.utils import getNextDirection
from snakeGame.ui_elements import ScoreText

from snakeGame.setup import FPS, TPS, GP_BACKGROUND_COLOR

def gameplayLoop(window: pygame.Surface, loop: bool, snake, grid, foodList, hotSpotList, clock: pygame.time.Clock) -> bool:
    """
    Main gameplay loop for the Snake game.
    Args:
        window (pygame.Surface): The game window surface.
        loop (bool): Flag indicating whether the game loop should continue.
        clock (pygame.time.Clock): The game clock object.
    Returns:
        bool: False when gameplay has ended (e.g., when the snake crashes).
    """
    
    gameTPS = TPS

    # Game Event timing (Ticks)
    timeStep = 1000 / gameTPS
    lastUpdateTime = pygame.time.get_ticks()
    deltaTime = timeStep
    

    direction = Vector2(1, 0) # Initial direction: right
    dQueue = [direction]
    won = False
    
    foodList.newRandomFood(snake, hotSpotList)
    
    
    SCORE_FONT = pygame.font.Font(None, 34)
    scoreColor = "blue"
    scoreText = ScoreText(screen=window, font=SCORE_FONT, color=scoreColor)
    
    
    wasGraceMove = False

    while loop:
        # Handle Events every frame
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    pass
                
                case pygame.KEYDOWN:
                    previousDir = direction if not dQueue else dQueue[-1]

                    nextDir = getNextDirection(previousDir=previousDir, event=event)
                    if len(dQueue) < 2:
                        dQueue.append(nextDir)
                        
                case _:
                    pass
                
        
        
        # Game Ticks
        while deltaTime >= timeStep:
            # Update snake position every tick:
            # Process game updates based on the fixed timestep.
            # If more than one time step has passed since the last tick, update the game.
            # The while loop ensures that the game catches up if it freezes for more than two time steps.
            # It will then run multiple updates until the position is correct based on the time passed.
            direction = dQueue.pop(0) if len(dQueue) > 0 else direction
                
            died, moved, won = snake.move(direction, previousWasGraceMove=wasGraceMove)
            wasGraceMove = not moved
            
            loop = not (died or won)
            
            deltaTime -= timeStep
            lastUpdateTime += timeStep
            gameTPS = np.sqrt(snake.score)
            
        currentTime = pygame.time.get_ticks()
        deltaTime = currentTime - lastUpdateTime
        
        timeStep = 1000 / gameTPS

        # Render the screen with all elements, every frame.
        window.fill(GP_BACKGROUND_COLOR)

        scoreText.draw(snake.score)
        
        grid.draw(window)
        foodList.draw()
        hotSpotList.draw()
        
        snake.draw()

        pygame.display.flip()
        
        # Cap the frame rate to FPS
        clock.tick(FPS)
    
    # Return False when gameplay has ended (crashed etc.) 
    return won, died
