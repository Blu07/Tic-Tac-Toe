from pygame import Vector2


class ScoreText:
    
    text = "Score"
    width = 150
    
    def __init__(self, screen, font, color):
        """
        Initializes a Score text object.

        Args:
            screen (pygame.Surface): The game window surface.
            font (pygame.font.Font): The font used for the text.
            color (tuple): The color of the text in RGB format.
        """
        
        self.font = font
        self.color = color
        self.screen = screen
        
        # Calculate the position of the text based on the screen size
        self.pos = Vector2(screen.get_width() - self.width, 50)
        
        
    def draw(self, score: int):
        """Draw the score on the screen.
        """
        
        scoreText = f"{self.text}: {score}"
        self.textSurf = self.font.render(scoreText, True, self.color)  # Rendered text surface
        
        self.screen.blit(self.textSurf, self.pos)
        
