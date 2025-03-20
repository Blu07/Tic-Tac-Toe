from pygame.math import Vector2

class Text:
    
    def __init__(self, screen, font, text, color, bgColor=None, center: Vector2 = None, topLeftPos: Vector2 = None):
        
        self.screen = screen
        self.font = font
        
        self.text = text
        self.color = color
        self.bgColor = bgColor
        
        
        self.textSurf = self.font.render(text, True, self.color)  # Rendered text surface
        
        if center:
            self.topLeftPos = Vector2(center.x - self.textSurf.get_width() // 2, center.y - self.textSurf.get_height() // 2)
        elif topLeftPos:
            self.topLeftPos = topLeftPos
        else:
            topLeftPos = Vector2(0, 0)
            
        
    
    def draw(self):
        """Draw the text on the screen.
        """
        
        self.screen.blit(self.textSurf, self.topLeftPos)
        
