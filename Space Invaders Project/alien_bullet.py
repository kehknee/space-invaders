import pygame
from pygame.sprite import Sprite

class AlienBullet(pygame.sprite.Sprite):
    
    def __init__(self, ai_game, alien):
        """Create a bullet at the alien's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.color = (255, 0, 0)  
        self.speed = 3.0
        self.rect = pygame.Rect(0, 0, 3, 15)  
        self.rect.midtop = alien.rect.midbottom  
        self.y = float(self.rect.y)  

    def update(self):
        """Move the bullet down."""
        self.y += self.speed  
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
