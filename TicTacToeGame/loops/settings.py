import pygame
from pygame.math import Vector2

from common.setup import FPS, BG_COLOR
from common.ui_elements import SettingText, SettingButton, Button, Text


def setSettings(window, clock, initSettings):
    """
    Settings screen for the Tic Tac Toe game.
    
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock object.
    """
    
    # Set up the game window
    pygame.init()
    
    pygame.display.set_caption("Settings for Tic Tac Toe")
    
    
    settings = initSettings
    center = Vector2(window.get_width() // 2, window.get_height() // 2)
    
    
    # Initalize Text elements
    titleText = Text(
        window,
        "Settings",
        pygame.font.Font(None, 50),
        "black",
        center = center + Vector2(0, -300)
    )

    # Text elements for the current settings
    textFont = pygame.font.Font(None, 36)
    
    gridSizeXText = SettingText(window, textFont, "Grid Size X", settings['grid_size_x'], (0, 0, 0), center=center + Vector2(-100, -200))
    gridSizeYText = SettingText(window, textFont, "Grid Size Y", settings['grid_size_y'], (0, 0, 0), center=center + Vector2(-100, -150))
    winLengthText = SettingText(window, textFont, "Win Length", settings['win_length'], (0, 0, 0), center=center + Vector2(-100, -100))
    playerXtext = SettingText(window, textFont, "Player X", settings['playerX'], (0, 0, 0), center=center + Vector2(-100, -50))
    playerOtext = SettingText(window, textFont, "Player O", settings['playerO'], (0, 0, 0), center=center + Vector2(-100, 0))

    
    
    # Initialize Buttons
    buttonFont = pygame.font.Font(None, 36)
    buttonTextColor = (255, 255, 255)
    buttonColor = (0, 0, 255)
    buttonPadding = Vector2(10, 10)
    
    
    increaseSizeX = SettingButton(window, "+1", buttonFont, buttonColor, buttonTextColor, center + Vector2(100, -200), buttonPadding, lambda s: s.update({"grid_size_x": min(10, s["grid_size_x"] + 1)}), "grid_size_x", gridSizeXText)
    decreaseSizeX = SettingButton(window, "-1", buttonFont, buttonColor, buttonTextColor, center + Vector2(50, -200), buttonPadding, lambda s: s.update({"grid_size_x": max(1, s["grid_size_x"] - 1)}), "grid_size_x", gridSizeXText)
    
    increaseSizeY = SettingButton(window, "+1", buttonFont, buttonColor, buttonTextColor, center + Vector2(100, -150), buttonPadding, lambda s: s.update({"grid_size_y": min(10, s["grid_size_y"] + 1)}), "grid_size_y", gridSizeYText)
    decreaseSizeY = SettingButton(window, "-1", buttonFont, buttonColor, buttonTextColor, center + Vector2(50, -150), buttonPadding, lambda s: s.update({"grid_size_y": max(1, s["grid_size_y"] - 1)}), "grid_size_y", gridSizeYText)

    increaseWinLen = SettingButton(window, "+1", buttonFont, buttonColor, buttonTextColor, center + Vector2(100, -100), buttonPadding, lambda s: s.update({"win_length": s["win_length"] + 1}), "win_length", winLengthText)
    decreaseWinLen = SettingButton(window, "-1", buttonFont, buttonColor, buttonTextColor, center + Vector2(50, -100), buttonPadding, lambda s: s.update({"win_length": max(1, s["win_length"] - 1)}), "win_length", winLengthText)

    setPlayerXHuman = SettingButton(window, "Human", buttonFont, buttonColor, buttonTextColor, center + Vector2(75, -50), buttonPadding, lambda s: s.update({"playerX": "Human"}), "playerX", playerXtext)
    setPlayerXAI = SettingButton(window, "AI", buttonFont, buttonColor, buttonTextColor, center + Vector2(150, -50), buttonPadding, lambda s: s.update({"playerX": "AI"}), "playerX", playerXtext)
    
    setPlayerOHuman = SettingButton(window, "Human", buttonFont, buttonColor, buttonTextColor, center + Vector2(75, 0), buttonPadding, lambda s: s.update({"playerO": "Human"}), "playerO", playerOtext)
    setPlayerOAI = SettingButton(window, "AI", buttonFont, buttonColor, buttonTextColor, center + Vector2(150, 0), buttonPadding, lambda s: s.update({"playerO": "AI"}), "playerO", playerOtext)


    settingTexts = [
        gridSizeXText, gridSizeYText, winLengthText, playerXtext, playerOtext
    ]
    
    settingButtons = [
        increaseSizeX, increaseSizeY, decreaseSizeX, decreaseSizeY,
        increaseWinLen, decreaseWinLen,
        setPlayerXHuman, setPlayerXAI,
        setPlayerOHuman, setPlayerOAI
    ]
    
    
    
    
    # Start game Button
    startButton = Button(window, "Start Game!", buttonFont, buttonColor, buttonTextColor, center=center + Vector2(0, 200), padding=buttonPadding)

    
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ready = True
                    break
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for button in settingButtons:
                    if button.isPressed(event.pos):
                        button.click(settings)
                
                if startButton.isPressed(event.pos):
                    ready = True
                    return settings

                
    
        window.fill(BG_COLOR)
        
        titleText.draw()
        startButton.draw()
    
        # Draw the current settings and related buttons
        for settingText in settingTexts:
            settingText.draw()
        
        for button in settingButtons:
            button.draw()
    
        pygame.display.flip()
        
        clock.tick(FPS)
    
    

    return settings