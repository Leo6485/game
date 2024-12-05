import pygame as pg
from cursor import Cursor
from settings import GREEN
from arma import Weapon

class Player:
    vel = 0.025

    def __init__(self):
        self.pos = pg.Vector2(400, 400)
        self.size = 25
        self.life = 100
        self.is_fire = 0
        self.with_flag = 0
        self.arma = Weapon(self)

        self.cursor = Cursor()

        self.player_id = self.connect("Player_name")
        self.team = self.player_id % 2

    def connect(self, name):
        return 0  # Simula conexão

    def update(self, pressed, mouse_pressed):
        self.cursor.update()
        if pressed[pg.K_w]:
            self.pos.y += self.cursor.delta.y * self.vel
            self.pos.x += self.cursor.delta.x * self.vel
        
        self.arma.update(mouse_pressed)

    def draw(self, screen):
        # Player
        pg.draw.rect(screen, (0, 255, 0), (*self.pos, self.size, self.size))

        # Cursor
        pg.draw.circle(screen, (0, 255, 0), ((self.pos.x + self.cursor.pos.x + 25/2), (self.pos.y + self.cursor.pos.y + 25/2)), 5)

        # Arma
        self.arma.draw(screen)
