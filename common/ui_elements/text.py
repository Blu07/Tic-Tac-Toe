from pygame.math import Vector2

class Text:
    
    def __init__(self, screen, text, font, color, bgColor=None, center: Vector2 = None, topLeftPos: Vector2 = None):
        
        self.screen = screen
        self.font = font
        
        self.text = text
        self.color = color
        self.bgColor = bgColor
        
        self.center = center
        
        self.topLeftPos = topLeftPos
        
        self.render()
    
    
    def updateText(self, newText: str):
        
        self.text = newText
        self.render()
        
    
    def render(self):
        
        self.textSurf = self.font.render(self.text, True, self.color)
        
        if self.center:
            self.topLeftPos = Vector2(
                self.center.x - self.textSurf.get_width() // 2,
                self.center.y - self.textSurf.get_height() // 2
            )
            
        else:
            # Default to top left corner of screen.
            self.topLeftPos = Vector2(0, 0)
        
    
    def draw(self):
        """Draw the text on the screen.
        """
        
        self.screen.blit(self.textSurf, self.topLeftPos)
        



class SettingText(Text):
    def __init__(self, window, font, label, initValue, color, center):
        self.label = label
        self.value = initValue
        text = f"{label}: {initValue}"
        
        super().__init__(window, text, font, color, center=center)
    
    def updateValue(self, newValue):
        """Update the value of the setting text.
        Args:
            newValue (str): The new value to set.
        """
        self.value = newValue
        self.text = f"{self.label}: {newValue}"
        self.render()
