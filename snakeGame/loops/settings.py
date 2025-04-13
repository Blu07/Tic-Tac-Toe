import pygame
from pygame.math import Vector2

from common.setup import FPS, BG_COLOR
from common.ui_elements import LabelText, SettingButton, Button, Text

from ..setup import MIN_GRID_SIZE, MAX_GRID_SIZE


def settingsLoop(window, clock, initSettings):
    """
    Settings screen for the Snake game.
    
    Args:
        window (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock object.
    """
    
    # Set up the game window
    pygame.init()
    
    pygame.display.set_caption("Settings for Snake")
    
    
    settings = initSettings
    center = Vector2(window.get_width() // 2, window.get_height() // 2)
    
    
    # Initalize Text elements
    titleText = Text(
        window,
        "Settings for Snake",
        pygame.font.Font(None, 50),
        "black",
        center = center + Vector2(0, -300)
    )

    # Text elements for the current settings
    textFont = pygame.font.Font(None, 36)
    
    gridSizeXText = LabelText(window, textFont, "Grid Size X", settings['grid_size_x'], (0, 0, 0), center=center + Vector2(-100, -200))
    gridSizeYText = LabelText(window, textFont, "Grid Size Y", settings['grid_size_y'], (0, 0, 0), center=center + Vector2(-100, -150))

    
    
    # Initialize Buttons
    buttonFont = pygame.font.Font(None, 36)
    buttonTextColor = "white"
    buttonColor = (0, 128, 255)
    buttonPadding = Vector2(20, 20)
    buttonBorderRadius = 10
    
    
    increaseSizeX1 = SettingButton(window, "+1", buttonFont, buttonColor, buttonTextColor, center + Vector2(150, -200), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_x": min(MAX_GRID_SIZE, s["grid_size_x"] + 1)}), "grid_size_x", gridSizeXText)
    increaseSizeX10 = SettingButton(window, "+10", buttonFont, buttonColor, buttonTextColor, center + Vector2(215, -200), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_x": min(MAX_GRID_SIZE, s["grid_size_x"] + 10)}), "grid_size_x", gridSizeXText)
    
    decreaseSizeX1 = SettingButton(window, "-1", buttonFont, buttonColor, buttonTextColor, center + Vector2(95, -200), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_x": max(MIN_GRID_SIZE, s["grid_size_x"] - 1)}), "grid_size_x", gridSizeXText)
    decreaseSizeX10 = SettingButton(window, "-10", buttonFont, buttonColor, buttonTextColor, center + Vector2(35, -200), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_x": max(MIN_GRID_SIZE, s["grid_size_x"] - 10)}), "grid_size_x", gridSizeXText)
    
    increaseSizeY1 = SettingButton(window, "+1", buttonFont, buttonColor, buttonTextColor, center + Vector2(150, -150), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_y": min(MAX_GRID_SIZE, s["grid_size_y"] + 1)}), "grid_size_y", gridSizeYText)
    increaseSizeY10 = SettingButton(window, "+10", buttonFont, buttonColor, buttonTextColor, center + Vector2(215, -150), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_y": min(MAX_GRID_SIZE, s["grid_size_y"] + 10)}), "grid_size_y", gridSizeYText)
    
    decreaseSizeY1 = SettingButton(window, "-1", buttonFont, buttonColor, buttonTextColor, center + Vector2(95, -150), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_y": max(MIN_GRID_SIZE, s["grid_size_y"] - 1)}), "grid_size_y", gridSizeYText)
    decreaseSizeY10 = SettingButton(window, "-10", buttonFont, buttonColor, buttonTextColor, center + Vector2(35, -150), buttonPadding, buttonBorderRadius, lambda s: s.update({"grid_size_y": max(MIN_GRID_SIZE, s["grid_size_y"] - 10)}), "grid_size_y", gridSizeYText)


    settingTexts = [
        gridSizeXText, gridSizeYText
    ]
    
    settingButtons = [
        increaseSizeX1, increaseSizeX10, decreaseSizeX1, decreaseSizeX10,
        increaseSizeY1, increaseSizeY10, decreaseSizeY1, decreaseSizeY10
    ]
    
    
    
    
    # Start game Button
    startButton = Button(window, "Start Game!", buttonFont, buttonColor, buttonTextColor, center=center + Vector2(0, -50), padding=buttonPadding, borderRadius=buttonBorderRadius)
    backButton = Button(window, "Back to Menu", buttonFont, buttonColor, buttonTextColor, center=Vector2(110, 50), padding=buttonPadding, borderRadius=buttonBorderRadius)

    
    loop = True
    while loop:
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
                    loop = False
                    navigation = "game"
                    break
                    
                if backButton.isPressed(event.pos):
                    loop = False
                    navigation = "menu"
                    break

                
    
        window.fill(BG_COLOR)
        
        titleText.draw()
        startButton.draw()
        backButton.draw()
    
        # Draw the current settings and related buttons
        for settingText in settingTexts:
            settingText.draw()
        
        for button in settingButtons:
            button.draw()
    
        pygame.display.flip()
        
        clock.tick(FPS)
    

    return settings, navigation