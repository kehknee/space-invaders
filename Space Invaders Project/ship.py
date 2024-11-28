import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Movement flags; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # Load the explosion frames of the ship
        self.explosion_frames = [ pygame.image.load('images/ship_boom0.png'), 
                                  pygame.image.load('images/ship_boom1.png'), 
                                  pygame.image.load('images/ship_boom2.png') ]
        
        # Ship explosion settings
        self.exploding = False
        self.explosion_index = 0
        self.explosion_timer = pygame.time.get_ticks()
        self.explosion_delay = 100
        self.explosion_done = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def _play_explosion(self):
        """Play the explosion animation frame by frame."""
        current_time = pygame.time.get_ticks()

        if current_time - self.explosion_timer > self.explosion_delay:
            self.explosion_timer = current_time
            self.explosion_index += 1

            if self.explosion_index >= len(self.explosion_frames):
                
                self.exploding = False  
                self.explosion_done = True  
                self.explosion_index = len(self.explosion_frames) - 1  
                
                return

        # Display the current explosion frame
        if self.explosion_index < len(self.explosion_frames):
            self.screen.blit(self.explosion_frames[self.explosion_index], self.rect)

    def start_explosion(self):
        """Start the explosion animation for the ship."""
        self.exploding = True
        self.explosion_index = 0  
        self.explosion_timer = pygame.time.get_ticks()  
        self.explosion_done = False  

    def update(self):
        """Update the ship's position based on movement flags."""
        
        if self.exploding:
            self._play_explosion()
        else:
            # Update the ship's x value, not the rect.
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.x -= self.settings.ship_speed
            if self.moving_up and self.rect.top > 0:
                self.y -= self.settings.ship_speed
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ship_speed
            
            # Update rect object from self.x.
            self.rect.x = self.x
            self.rect.y = self.y

    def blitme(self):
        """Draw the ship or the explosion at its current location."""
        if not self.exploding:
            self.screen.blit(self.image, self.rect)