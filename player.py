import pygame as pg
from cursor import Cursor
from settings import GREEN
from arma import ArmaBalanco, EspadaDireta

class Player:
    vel = 0.025

    def __init__(self, id):
        self.pos = pg.Vector2(400, 400)
        self.size = 25
        self.life = 100
        self.is_fire = 0
        self.with_flag = 0
        self.armas = [ArmaBalanco(self), EspadaDireta(self)]
        self.arma_atual = 0

        self.cursor = Cursor()

        self.name = "Player_name"
        self.name_text = pg.font.Font(None, 20).render(self.name, True, (255, 255, 255))
        self.id = id # self.connect(self.name)
        self.team = self.id % 2

    def connect(self, name):
        return 0  # Simula conexão
    
    def troca_arma(self):
        self.arma_atual = (self.arma_atual + 1) % len(self.armas)


    def update(self, pressed, mouse_pressed):
        self.cursor.update()
        if pressed[pg.K_w]:
            self.pos.y += self.cursor.pos.y * self.vel
            self.pos.x += self.cursor.pos.x * self.vel
        
        self.armas[self.arma_atual].update(mouse_pressed)

    def draw(self, screen):
        # Cursor
        pg.draw.circle(screen, (0, 255, 0), ((self.pos.x + self.cursor.pos.x + 25/2), (self.pos.y + self.cursor.pos.y + 25/2)), 5)

        # Player
        pg.draw.rect(screen, (0, 255, 0) if not self.team else (255, 0, 0), (*self.pos, self.size, self.size))

        # Arma
        self.armas[self.arma_atual].draw(screen)
        
        # Nome
        text_rect = self.name_text.get_rect(center=(self.pos.x, self.pos.y - self.size/2 - 5))
        screen.blit(self.name_text, text_rect)