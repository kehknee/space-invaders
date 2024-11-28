import pygame as pg
from pygame.sprite import Sprite, Group


BARRIER_ARCH_HEIGHT = 4 
BARRIER_ARCH_WIDTH_2 = 4

class BarrierPiece(Sprite):
    color = 255, 0, 0
    black = 0, 0, 0
    health_colors = {6: pg.Color(0, 255, 0),
                     5: pg.Color(0, 128, 255),
                     4: pg.Color(0, 0, 255),
                     3: pg.Color(255, 255, 0),
                     2: pg.Color(255, 128, 0),
                     1: pg.Color(255, 0, 0),
                     0: pg.Color(0, 0, 0)}

    def __init__(self, ai_game, rect):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.rect = rect
        self.health = len(BarrierPiece.health_colors) - 1

    def hit(self):
        #print('BarrierPiece hit!')
        if self.health > 0: 
            self.health -= 1
        if self.health == 0: self.kill()

    def update(self): pass

    def draw(self):
        pg.draw.rect(self.screen, BarrierPiece.health_colors[self.health], self.rect)
        # pg.draw.rect(self.screen, pg.Color(0, 255, 0), self.rect)


class Barrier(Sprite):    # not a real Barrier class -- should be made up of many tiny Sprites
                          # you will not get credit for this class unless it is updated to tiny Sprites
    def __init__(self, ai_game, width, height, deltax, deltay, x, y):
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        # self.rect = rect

        self.width, self.height = width, height
        self.x, self.y = x, y
        self.deltax, self.deltay = deltax, deltay
        self.settings = ai_game.settings
        self.ship_lasers = ai_game.bullets
        self.fleet = ai_game.aliens
        self.fleet_lasers = ai_game.alien_bullets
        self.barrier_pieces = Group()
        self.create_barrier_pieces()

    def create_barrier_pieces(self):
        left, top = 0, 0
        height, width = int(self.height/self.deltax), int(self.width/self.deltay)
        for i in range(height):
        # for i in range(int(self.height/self.deltax)):
            # for j in range(int(self.width/self.deltay)):
            for j in range(width):
                rect = pg.Rect(self.x + left + j * self.deltax, 
                               self.y + top + i * self.deltay, 
                               self.deltax, self.deltay)
                
                if height - i < BARRIER_ARCH_HEIGHT and abs(j - width/2) < BARRIER_ARCH_WIDTH_2: 
                    continue     # don't print middle of arch
                self.barrier_pieces.add(BarrierPiece(ai_game=self.ai_game, rect=rect))


    def reset(self):
        self.barrier_pieces.empty()
        self.create_barrier_pieces()

    def is_dead(self): return self.health == 0

    def update(self): 
        collisions = pg.sprite.groupcollide(self.barrier_pieces, self.ai_game.bullets, False, True)
        for c in collisions:
            c.hit()
        alien_collisions = pg.sprite.groupcollide(self.barrier_pieces, self.ai_game.alien_bullets, True, True)
        for piece in alien_collisions:
            piece.hit()
        
        self.draw()

    def draw(self):
        for bp in self.barrier_pieces:
            bp.draw()


BARRIER_WIDTH = 150
BARRIER_HEIGHT = 80

class Barriers:
    positions = [(BARRIER_WIDTH * x + BARRIER_WIDTH / 2.0, 600) for x in range(0, 7, 2)]
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.barriers = Group()
        self.create_barriers()

    def create_barriers(self):     
        width = self.settings.screen_width / 10
        height = 2.0 * width / 4.0
        top = self.settings.screen_height - 2.1 * height
                
        barriers = [Barrier(ai_game=self.ai_game, 
                            width=BARRIER_WIDTH, height=BARRIER_HEIGHT, 
                            deltax=10, deltay=10,                            # smaller is smaller piedes
                            # deltax=20, deltay=20, 
                            x=x, y=y) for x, y in Barriers.positions]
        for barrier in barriers:
            self.barriers.add(barrier)

    def hit(self): pass 
    
    def reset(self):
        for barrier in self.barriers:
            barrier.reset()

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers: 
            barrier.draw()

