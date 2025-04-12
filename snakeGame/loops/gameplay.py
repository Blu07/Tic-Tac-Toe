import pygame
from pygame.font import Font
from pygame.math import Vector2

import sys
import numpy as np

from common.utils import getNextDirection, dir2Vec
from common.ui_elements import LabelText
from common.setup import FPS, GAMEPLAY_BG_COLOR

from snakeGame.setup import TPS

def gameplayLoop(window: pygame.Surface, snake, grid, foodList, hotSpotList, clock: pygame.time.Clock) -> bool:
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
    
    
    # Show the score in the top right corner
    scoreText = LabelText(
        window,
        font = Font(None, 34),
        label = "Score",
        initValue = snake.score,
        color = "blue",
        center = Vector2(window.get_width() - 150, 50),
    )
    

    direction = dir2Vec("right")
    dQueue = [direction] # Direction queue for snake movement.
    won = False
    
    foodList.newRandomFood(snake, hotSpotList)
    
    wasGraceMove = False
    
    terminal = False
    while not terminal:
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
            
            terminal = died or won
            
            deltaTime -= timeStep
            lastUpdateTime += timeStep
            gameTPS = np.sqrt(snake.score)
            
            scoreText.updateValue(snake.score)
            
        currentTime = pygame.time.get_ticks()
        deltaTime = currentTime - lastUpdateTime
        
        timeStep = 1000 / gameTPS

        # Render the screen with all elements, every frame.
        window.fill(GAMEPLAY_BG_COLOR)

        
        scoreText.draw()
        
        grid.draw(window)
        foodList.draw()
        hotSpotList.draw()
        
        snake.draw()

        pygame.display.flip()
        
        # Cap the frame rate to FPS
        clock.tick(FPS)
    
    # return the result of the game
    return "game_over" if died else "won"
