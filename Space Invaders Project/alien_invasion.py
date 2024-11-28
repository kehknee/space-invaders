# Kenneth Tran
# Aliens and ship images provided by Prof. McCarthy
# Sounds gotten from YouTube
# Barrier class also provided by Prof. McCarthy, except for small changes
# Code adapted from Python Crash Course book

import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from event import Event
from alien_bullet import AlienBullet
from ufo import UFO
from barrier import Barriers
import random


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.aliens_moving = True
        self.ship_exploding = False
        
        # Load sounds for background music and shooting.
        self.shoot_sound = pygame.mixer.Sound('Sounds/shoot_sound.mp3')
        self.ufo_sound = pygame.mixer.Sound('Sounds/ufo_sound.mp3')
        self.ufo_sound.set_volume(0.4)
        pygame.mixer.music.load('Sounds/music_loop.mp3')
        pygame.mixer.music.play(-1)

        # Make settings for UFO.
        self.ufo = UFO(self)  
        self.ufo_active = False  
        self.ufo_spawn_timer = 0  
        self.ufo_destroyed_position = None
        self.ufo_destroyed_display_time = None

        # Initiate barriers.
        self.barrier = Barriers(self)

        # Create fleet of aliens.   
        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")
        
        # Make High Score button.
        self.high_score_button = Button(self, "High Score")
        self.high_score_screen = False
             
        self.event = Event(self)
    
        # Font for the title and alien points display.
        self.title_font = pygame.font.SysFont(None, 80)  # For the game title
        self.alien_font = pygame.font.SysFont(None, 40)  # For alien point values

        # Define alien images for main menu
        self.alien_images = [
            pygame.image.load('images/alien00.png'),
            pygame.image.load('images/alien10.png'),
            pygame.image.load('images/alien20.png')
            ]

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.event._check_events()

            # Option to open high score menu.
            if self.high_score_screen:
                self._show_high_score_screen()

            else:
                if self.game_active:
                    self.ship.update()
                    
                    # Move to ship exploding function if true.
                    if self.ship_exploding:
                        if self.ship.explosion_done:
                            self._ship_hit()                        
                    else:
                        self._update_bullets()
                        self._update_aliens()
                        self._update_ufo()
                        self._check_bullet_ufo_collisions()  
                        self.barrier.update()         

                self._update_screen()
                
            self.clock.tick(60)

    def _update_ufo(self):
        """Spawn UFO at random time intervals, play a sound, and remove it when off screen."""
        if not self.ufo_active:
            # Randomly spawn the UFO every few seconds, and play the sounds.
            if pygame.time.get_ticks() - self.ufo_spawn_timer > random.randint(5000, 10000): 
                self.ufo_active = True
                self.ufo_spawn_timer = pygame.time.get_ticks()  
                self.ufo.reset_position()
                self.ufo_sound.play(-1)
                
        if self.ufo_active:
            self.ufo.update()

            # Check if the UFO has gone off-screen and kill it, as well as stopping the sound.
            if self.ufo.rect.left > self.settings.screen_width or self.ufo.rect.right < 0:
                self.ufo_active = False
                self.ufo_spawn_timer = pygame.time.get_ticks()
                self.ufo_sound.stop()

    def _check_bullet_ufo_collisions(self):
        """Check if any bullet has hit the UFO"""
        if self.ufo_active:
            # Check for collision between bullets and the UFO
            collisions = pygame.sprite.spritecollide(self.ufo, self.bullets, True)
            if collisions:
                
                self.ufo_destroyed_position = self.ufo.rect.topleft
                self.ufo_destroyed_display_time = pygame.time.get_ticks()
                
                # Give the user the score, display the score, and stop the sound.
                self.stats.score += self.settings.ufo_points  
                self.sb.prep_score()  
                self.sb.check_high_score()  
                
                self.ufo_active = False  
                self.ufo_spawn_timer = pygame.time.get_ticks()  
                self.ufo_sound.stop()
                
                
                
                print(f"UFO hit! +{self.settings.ufo_points} points")

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        if collisions:
            # Give points when aliens are hit with bullets.
            for aliens in collisions.values():   
                # for alien in aliens:
                #     alien.start_explosion() 
                                          
                self.stats.score += self.settings.alien_points * len(aliens)    
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        
        # Check if the explosion is done only after the ship has started exploding
        if self.ship.explosion_done and self.ship_exploding:
            if self.stats.ships_left > 0:
                # Decrement ship lives left, and update scoreboard.
                self.stats.ships_left -= 1
                if self.stats.ships_left == 0:
                    self.game_active = False
                    pygame.mouse.set_visible(True)
                    self.ufo_sound.stop()
                    self.ufo_active = False
                    print("Game over.")
                self.sb.prep_ships()

                # Get rid of any remaining bullets and aliens.
                self.bullets.empty()
                self.aliens.empty()

                # Create a new fleet and center the ship.
                self._create_fleet()
                self.ship.center_ship()
                
                self.aliens_moving = True
                self.ship_exploding = False
                
                # Pause.
                sleep(0.5)
                 
    def _ship_explosion_start(self):
        if not self.ship.exploding and self.stats.ships_left > 0:
            # Start the explosion when hit
            self.ship.start_explosion()
            self.aliens_moving = False
            self.ship_exploding = True

# Alien Functions

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        if self.aliens_moving:
            self._check_fleet_edges()
            self.aliens.update()

            # Look for alien-ship collisions.
            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()

            # Look for aliens hitting the bottom of the screen.
            self._check_aliens_bottom()
        
        # Aliens randomly shoot bullets that can collide with ship and barriers.
        for alien in self.aliens.copy():
            if random.randint(1, 3000) == 1:
                self._alien_fires_bullet(alien)
                
        self._update_alien_bullets()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height and self.stats.ships_left > 0:
                # Treat this the same as if the ship got hit.
                self._ship_explosion_start()
                break
            elif alien.rect.bottom >= self.ship.rect.top and self.stats.ships_left > 0:
                self._ship_explosion_start()
                break

    def _create_fleet(self):
        """Create the fleet of aliens."""
        spacing = 1.9
        # Create an alien and keep adding aliens until there's no room left.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - spacing * alien_width):
                self._create_alien(current_x, current_y)
                current_x += spacing * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += spacing * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _alien_fires_bullet(self, alien):
        """Create a new bullet and add it to the group to be fired."""
        new_bullet = AlienBullet(self, alien)
        self.alien_bullets.add(new_bullet)
        
    def _update_alien_bullets(self):
        """Check if bullets have collided with ship."""
        self.alien_bullets.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            self._ship_explosion_start()
            
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)
                
# Main Menu Functions

    def _draw_game_title(self):
        """Initiate game title"""
        title_text = self.title_font.render("Space Invaders", True, (255, 255, 255))
        title_rect = title_text.get_rect()
        title_rect.centerx = self.screen.get_rect().centerx
        title_rect.top = 50
        self.screen.blit(title_text, title_rect)

    def _draw_alien_points(self):
        """Draw alien and the corresponding points for main menu."""
        spacing = 50
        start_y = 200
        text_color = (255, 255, 255)

        for i, alien_image in enumerate(self.alien_images):
            # Draw the 3 different alien images
            alien_rect = alien_image.get_rect()
            alien_rect.x = 200  
            alien_rect.y = start_y + (alien_rect.height + spacing) * i
            self.screen.blit(alien_image, alien_rect)

            # Display the points next to the aliens
            points_text = f"= {self.settings.alien_points} points"
            points_surface = self.alien_font.render(points_text, True, text_color)
            points_rect = points_surface.get_rect()
            points_rect.left = alien_rect.right + 20  
            points_rect.centery = alien_rect.centery
            self.screen.blit(points_surface, points_rect)
          
        # Draw the UFO image  
        ufo_image = pygame.image.load('images/ufo.png')
        ufo_image = pygame.transform.scale(ufo_image, (50, 30)) 
        ufo_rect = ufo_image.get_rect()
        ufo_rect.x = 210
        ufo_rect.y = 540
        self.screen.blit(ufo_image, ufo_rect)

        # Display the UFO points next to the image
        ufo_points_text = f"= {self.settings.ufo_points} points"
        ufo_points_surface = self.alien_font.render(ufo_points_text, True, text_color)
        ufo_points_rect = ufo_points_surface.get_rect()
        ufo_points_rect.left = ufo_rect.right + 20  
        ufo_points_rect.centery = ufo_rect.centery
        self.screen.blit(ufo_points_surface, ufo_points_rect)
        
    def _show_high_score_screen(self):
        """Show the current high score when button is pressed."""
        self.screen.fill(self.settings.bg_color)
        
        high_score_text = f"High Score: {self.stats.load_high_scores()}"
        high_score_surface = self.title_font.render(high_score_text, True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50))
        self.screen.blit(high_score_surface, high_score_rect)
        
        pygame.display.flip()       
                           
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self.event._check_events()
        
        if not self.game_active:
            # If game is not active, show the main menu things
            
            self._draw_game_title()
            self._draw_alien_points()
            self.play_button.draw_button()
            self.high_score_button.draw_button()
            self.high_score_button.set_position(self.settings.screen_width // 2 - 100, self.settings.screen_height // 2 + 60)
                    
        else:
            if self.ufo_active:
                self.screen.blit(self.ufo.image, self.ufo.rect)
            
            if self.ufo_destroyed_position and pygame.time.get_ticks() - self.ufo_destroyed_display_time < 1000:
                ufo_destroyed_image = pygame.image.load('images/ufo_destroyed.png')
                ufo_destroyed_image = pygame.transform.scale(ufo_destroyed_image, (50, 30))
                self.screen.blit(ufo_destroyed_image, self.ufo_destroyed_position)
                
            if self.ship.exploding:
                self.screen.blit(self.ship.explosion_frames[self.ship.explosion_index], self.ship.rect)
            else:
                self.ship.blitme()
            
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
                
            for alien_bullet in self.alien_bullets.sprites():
                alien_bullet.draw_bullet()
                
            for alien in self.aliens.sprites(): 
                self.screen.blit(alien.image, alien.rect)
                        
            self.barrier.draw()
            #self.ship.blitme()
            #self.aliens.draw(self.screen)
            
            # Draw the score information.
            self.sb.show_score()
            
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()