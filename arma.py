import pygame as pg
from settings import *

class Weapon:
    def __init__(self, usuario):
        self.usuario = usuario
        self.scircular = False

    def update(self, mouse_pressed):
        pass

    def draw(self, screen):
        pass

class ArmaBalanco(Weapon):
    def __init__(self, usuario):
        super().__init__(usuario)
        self.usuario = usuario
        self.atq = False
        self.angulo_atq = 0
        self.vel_atq = 10
        self.duracao_atq = 30

    def update(self, mouse_pressed):
        if mouse_pressed[2]:
            if not self.atq:
                self.atq = True
                self.angulo_atq = -90
        
        if self.atq:
            self.angulo_atq += self.vel_atq
            if self.angulo_atq >= 90:  
                self.atq = False
                self.angulo_atq = 0
    
    def draw(self, screen):
        if self.atq:
            origem = (self.usuario.pos.x + self.usuario.size / 2, 
                      self.usuario.pos.y + self.usuario.size / 2)
            tamanho = 50
            fim_x = origem[0] + tamanho * pg.math.Vector2(1, 0).rotate(self.angulo_atq).x
            fim_y = origem[1] + tamanho * pg.math.Vector2(1, 0).rotate(self.angulo_atq).y

            pg.draw.line(screen, GREEN, origem, (fim_x, fim_y), 5)

class EspadaDireta(Weapon):
    def __init__(self, usuario):
        super().__init__(usuario)
        self.ataque = False
        self.distancia_atq = 0
        self.velocidade_ataque = 10

    def update(self, mouse_pressed):
        if mouse_pressed[2]:
            if not self.ataque:
                self.ataque = True
                self.distancia_atq = 0

        if self.ataque:
            self.distancia_atq += self.velocidade_ataque
            if self.distancia_atq >= 50:
                self.ataque = False
                self.distancia_atq = 0

    def draw(self, screen):
        if self.ataque:
            origem = (self.usuario.pos.x + self.usuario.size / 2, self.usuario.pos.y + self.usuario.size / 2)
            fim = (origem[0] + self.distancia_atq, origem[1])
            pg.draw.line(screen, GREEN, origem, fim, 5)