import pygame
from pygame.font import Font
import sys
import numpy as np

from common.utils import getNextDirection, dir2Vec
from common.ui_elements import ScoreText
from common.setup import FPS, GAMEPLAY_BG_COLOR

from snakeGame.setup import TPS

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
    
    # Game Event timing (Ticks)
    gameTPS = TPS
    timeStep = 1000 / gameTPS
    lastUpdateTime = pygame.time.get_ticks()
    deltaTime = timeStep
    

    direction = dir2Vec("right")
    dQueue = [direction] # Direction queue for snake movement.
    won = False
    
    foodList.newRandomFood(snake, hotSpotList)
    
    
    scoreText = ScoreText(
        window,
        font = Font(None, 34),
        color = "blue"
    )
    
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
        window.fill(GAMEPLAY_BG_COLOR)

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
