import pygame

from pygame.sprite import Sprite
import sys
from settings import Settings

import random

class UFO(pygame.sprite.Sprite):
    def __init__(self, ai_game):
        """Initialize the UFO and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the UFO image
        self.image = pygame.image.load('images/ufo.png')
        self.image = pygame.transform.scale(self.image, (50, 30))  

        self.rect = self.image.get_rect()
        self.direction = 1  

        # Start each new UFO off the screen
        self.reset_position()

    def reset_position(self):
        """Randomly choose whether UFO comes from the left or the right."""

        # Start UFO on the left
        if random.choice([True, False]):
            self.rect.x = -self.rect.width  
            self.direction = 1  
        else:
            # Start UFo on the right
            self.rect.x = self.settings.screen_width  
            self.direction = -1  

        self.rect.y = 60

    def update(self):
        """Move the UFO across the screen based on its direction."""
        self.rect.x += self.direction * self.settings.ufo_speed

        # If the UFO moves off the screen, remove it
        if self.rect.right < 0 or self.rect.left > self.settings.screen_width:
            self.kill() 

