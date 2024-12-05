import pygame as pg
from collections import namedtuple
from math import sqrt
from time import time




pg.init()
pg.display.set_caption("Jogo")
pg.mouse.set_visible(True)
clock = pg.time.Clock()


d = pg.display.Info()
DH = d.current_h
DW = d.current_w
del d

# ---- Cursor ---- #
class Cursor:
    def __init__(self):
        self.pos = pg.Vector2(0, 0)
        self.delta = pg.Vector2(0, 0)
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
            self.delta = self.pos.copy()
        elif dist <= self.limit:
            self.pos.x = dx
            self.pos.y = dy
            
            if dist:
                self.delta.x = dx/(dist/100)
                self.delta.y = dy/(dist/100)
            else:
                self.delta.x = 0
                self.delta.y = 0

        self.last_cursor_pos = pg.Vector2(pg.mouse.get_pos())
        
        # Atualiza a posição do cursor a cada 0.5 segundos para evitar lag
        if not (50 < self.last_cursor_pos.x < DW -50) or not (50 < self.last_cursor_pos.y < DH - 50):
            pg.mouse.set_pos(DW/2, DH/2)
            self.last_cursor_pos = pg.Vector2(DW/2, DH/2)

# ---- Player ---- #
class Player:
    vel = 0.025
    def __init__(self):
        self.pos = pg.Vector2(400, 400)
        self.size = 25
        self.life = 100
        self.is_fire = 0
        self.with_flag = 0

        self.cursor = Cursor()
        
        self.player_id = conn("Player_name")
        self.team = self.player_id % 2
    
    def update(self, pressed):
        self.cursor.update()
        if pressed[pg.K_w]:
            self.pos.y += self.cursor.delta.y * self.vel
            self.pos.x += self.cursor.delta.x * self.vel

    def draw(self, screen):
        # Player
        pg.draw.rect(screen, (0, 255, 0), (*self.pos, self.size, self.size))

        # Cursor
        pg.draw.circle(screen, (0, 255, 0), ((self.pos.x + self.cursor.pos.x + 25/2), (self.pos.y + self.cursor.pos.y + 25/2)), 5)

# ---- Game ---- #
class Game:
    def __init__(self):
        self.player = Player()
        self.players = {self.player.player_id: self.player}

        self.scale = min(DW/1200, DH/720)
        
        self.padding = ((DW - 1200 * self.scale) / 2, (DH - 720 * self.scale) / 2)

        self.screen = pg.Surface((1200, 720))
        self.final_screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    def update(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        pressed = pg.key.get_pressed()

        if pressed[pg.K_q]:self.running = False
        axis = [pressed[pg.K_s] - pressed[pg.K_w], pressed[pg.K_d] - pressed[pg.K_a]]

        self.player.update(pressed)

    def draw(self):
        self.screen.fill((20, 20, 20))
        self.final_screen.fill((0, 0, 0))

        draw_grid(self.screen, (0, 0, 0), 100)
        self.player.draw(self.screen)

        frame = pg.transform.scale(self.screen, (1200 * self.scale, 720 * self.scale))
        self.final_screen.blit(frame, self.padding)
        pg.display.flip()

    def run(self):
        self.running = True

        while self.running:
            self.update()
            self.draw()
            clock.tick(60)



# Simula uma conexão, retorna o id 0
def conn(name):
    return 0

def draw_grid(surface, color, cell_size):
    width, height = surface.get_size()
    for x in range(0, width, cell_size):
        pg.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pg.draw.line(surface, color, (0, y), (width, y))


game = Game()
game.run()