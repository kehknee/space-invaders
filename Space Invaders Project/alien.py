import pygame

from pygame.sprite import Sprite
from timer import Timer
from random import randint


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""
    n = 0
    alien_images0 = [pygame.image.load(f"images/alien0{n}.png") for n in range(2)]
    alien_images1 = [pygame.image.load(f"images/alien1{n}.png") for n in range(2)]
    alien_images2 = [pygame.image.load(f"images/alien2{n}.png") for n in range(2)]
    alien_images = [alien_images0, alien_images1, alien_images2]
    alien_explosion_images = [pygame.image.load(f"images/alien_boom{n}.png") for n in range(3)]
    #alien_explosion_images = [pygame.image.load(f"images/alien_boom{n}.png") for n in range (3)]
    #alien_explosion = ["images/alien_boom0.png", "images/alien_boom1.png", "images/alien_boom2.png"]
    
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        type=randint(0, 2)
        self.type = type
        self.timer = Timer(images=Alien.alien_images[type], delta=(type+1)*300, start_index=type % 2)
        #self.explosion_timer = Timer(images=Alien.alien_explosion[explosion_type], start_index=Alien.n % 2, loop_continuously=False)
        #self.explosion_timer = Timer(images=Alien.alien_explosion_images, delta=100, loop_continuously=False)
        self.exploding = False
        self.exploded = False
        self.explosion_frame = 0
    
        self.image = self.timer.current_image()
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def start_explosion(self):

        self.exploding = True
        self.explosion_frame = 0
        self.play_explosion()

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def play_explosion(self):
        print(f"Explosion function now running")
        if self.explosion_frame < len (Alien.alien_explosion_images):
            print(f"Playing explosion frame {self.explosion_frame}")
            self.screen.blit(Alien.alien_explosion_images[self.explosion_frame], self.rect)
            self.explosion_frame += 1
        else:
            self.exploded = True
            self.kill()

    def update(self):
        """Move the alien right or left."""
        if not self.exploding:
            self.x += self.settings.alien_speed * self.settings.fleet_direction
            self.rect.x = self.x
            self.image = self.timer.current_image()   # auto drawn IF you have latest image
        else:
            self.play_explosion()
 
    def draw(self):
        self.screen.blit(self.image, self.rect)