import pygame as pg
from collections import namedtuple
from math import sqrt

pg.init()
pg.display.set_caption("Jogo")
pg.mouse.set_visible(True)

clock = pg.time.Clock()

def conn(name):
    return 0

def draw_grid(surface, color, cell_size):
    width, height = surface.get_size()
    for x in range(0, width, cell_size):
        pg.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pg.draw.line(surface, color, (0, y), (width, y))

class Cursor:
    def __init__(self):
        self.pos = pg.Vector2(pg.mouse.get_pos())
        self.last_cursor_pos = pg.Vector2(pg.mouse.get_pos())
        self.limit = 100
    def update(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())

        dx = self.pos.x + mouse_pos.x - self.last_cursor_pos.x
        dy = self.pos.y + mouse_pos.y - self.last_cursor_pos.y

        dist = sqrt(dx**2 + dy**2)
        if self.limit < dist < self.limit + 100:
            self.pos.x = dx/(dist/100)
            self.pos.y = dy/(dist/100)
        elif dist <= self.limit:
            self.pos.x = dx
            self.pos.y = dy

        self.last_cursor_pos = pg.Vector2(pg.mouse.get_pos())

class Player:
    vel = 0.1
    def __init__(self):
        self.pos = pg.Vector2(400, 400)
        self.life = 100
        self.is_fire = 0
        self.with_flag = 0
        
        self.cursor = Cursor()
        
        self.player_id = conn("Player_name")
        self.team = self.player_id % 2
    
    def update(self, axis):
        self.cursor.update()
        if axis[0] == -1:
            self.pos.y += self.cursor.pos.y * self.vel
            self.pos.x += self.cursor.pos.x * self.vel

    def draw(self, screen):
        pg.draw.rect(screen, (0, 255, 0), (*self.pos, 25, 25))
        
        pg.draw.circle(screen, (0, 255, 0), (self.pos.x + self.cursor.pos.x + 25/2, self.pos.y + self.cursor.pos.y + 25/2), 5)

class Game:
    def __init__(self):
        self.player = Player()
        self.players = {self.player.player_id: self.player}
        self.screen = pg.display.set_mode((1200, 720))
    
    def update(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        pressed = pg.key.get_pressed()

        if pressed[pg.K_q]:self.running = False
        axis = [pressed[pg.K_s] - pressed[pg.K_w], pressed[pg.K_d] - pressed[pg.K_a]]

        self.player.update(axis)

    def draw(self):
        self.screen.fill((20, 20, 20))
        draw_grid(self.screen, (0, 0, 0), 25)
        self.player.draw(self.screen)
        pg.display.flip()
    
    def run(self):
        self.running = True

        while self.running:
            self.update()
            self.draw()
            clock.tick(60)

game = Game()
game.run()
# Teste