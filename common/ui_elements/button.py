import pygame
from pygame.math import Vector2

from .text import Text

class Button:
    def __init__(self, screen, text, font, bgColor, textColor, center=None, padding: Vector2 = None, width: int = None, height: int = None, borderRadius: int = 0):
        """
        Initializes a Button object. Draws arectangle with text on top of it.
        
        Args:
            screen: The screen surface to render the button on.
            text: The text to display on the button.
            font: The font to use for the button text.
            bgColor: The background color of the button.
            textColor: The color of the button text.
            center: The center position of the button. If None, the button will be centered at (0, 0).
            padding: The padding to add to the button dimensions. If None, no padding will be added.
            width: The width of the button. If None, the width will be determined by the text width.
            height: The height of the button. If None, the height will be determined by the text height.
        """
        
        self.screen = screen
        self.font = font
        self.bgColor = bgColor
        self.textColor = textColor
        self.borderRadius = borderRadius
        

        # Create a Text object to display the text on the button
        if center:
            self.text = Text(screen, text, font, textColor, bgColor, center=center)
        else:
            center = Vector2(0, 0)
            self.text = Text(screen, text, font, textColor, bgColor, center=center)
        
        
        # Create a rectangle for the button
        if not width:
            width = self.text.textSurf.get_width()
        
        if not height:
            height = self.text.textSurf.get_height()
               
        if padding:
            width += padding.x
            height += padding.y

        self.rect = pygame.Rect(center.x - width // 2, center.y - height // 2, width, height) # find the top left corner of the rectangle based on the center and dimensions
    
    
    def draw(self):
        """Draw the button rectangle and the text.
        """
        # Draw the button rectangle
        pygame.draw.rect(self.screen, self.bgColor, self.rect, border_radius=self.borderRadius)
        # Draw the text on top of the button
        self.text.draw()
        

    def isPressed(self, pos):
        """Check if the position (pos) is within the bounding box of the button.
        """
        return self.rect.collidepoint(pos)


class SettingButton(Button):
    def __init__(self, window, text, font, color, textColor, center, padding, borderRadius, clickFunc, settingKey, settingText):
        super().__init__(window, text, font, color, textColor, center=center, padding=padding, borderRadius=borderRadius)
        self.clickFunc = clickFunc
        self.settingText = settingText
        self.settingKey = settingKey
    
    def click(self, settings):
        """Update the settings based on the button clicked.

        Args:
            settings (dict): The current settings dictionary.
        """
        self.clickFunc(settings)
        self.settingText.updateValue(settings[self.settingKey])
    
    def __call__(self):
        return self.setting

