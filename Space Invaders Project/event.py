import pygame as pg
import sys 

from button import Button

class Event:
    def __init__(self, ai_game):
        self.ai_game = ai_game 
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.sb = ai_game.sb 
        #self.game_active = ai_game.game_active
        self.bullets = ai_game.bullets
        self.aliens = ai_game.aliens
        self.ship = ai_game.ship
        self.play_button = ai_game.play_button
        self.sb_button = ai_game.high_score_button
        
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_high_score_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.ai_game.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.ai_game.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self.ai_game._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pg.mouse.set_visible(False)
            
            #self.game_active = True

    def _check_high_score_button(self, mouse_pos):
        """Check if the player has clicked to display the high score."""
        button_clicked = self.sb_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.ai_game.game_active:
            self.ai_game.high_score_screen = True

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_UP:
            self.ship.moving_up = True
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self.ai_game._fire_bullet()
            self.ai_game.shoot_sound.play()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pg.K_UP:
            self.ship.moving_up = False
        elif event.key == pg.K_DOWN:
            self.ship.moving_down = False
