import pygame as pg
from settings import *
from player import Player
from utils import *
from arma import Weapon

class Game:
    def __init__(self):
        self.player = Player()
        self.players = {self.player.player_id: self.player}

        self.scale = min(DW / 1200, DH / 720)

        self.padding = ((DW - 1200 * self.scale) / 2, (DH - 720 * self.scale) / 2)

        self.screen = pg.Surface((1200, 720))
        self.final_screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

    def update(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False

        pressed = pg.key.get_pressed()
        mouse_pressed = pg.mouse.get_pressed()
        
        if pressed[pg.K_q]: 
            self.running = False

        self.player.update(pressed, mouse_pressed)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.final_screen.fill(FINAL_BG_COLOR)

        draw_grid(self.screen, GRID_COLOR, 100)
        self.player.draw(self.screen)

        frame = pg.transform.scale(self.screen, (1200 * self.scale, 720 * self.scale))
        self.final_screen.blit(frame, self.padding)
        pg.display.flip()

    def run(self):
        self.running = True

        while self.running:
            self.update()
            self.draw()
            pg.time.Clock().tick(FPS)
