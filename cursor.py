import pygame as pg
from math import sqrt
from settings import DW, DH

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

        if self.limit < dist < self.limit + max(DW, DH):
            self.pos.x = dx / (dist / 100)
            self.pos.y = dy / (dist / 100)
            self.delta = self.pos.copy()

        elif dist <= self.limit:
            self.pos.x = dx
            self.pos.y = dy
           
            if dist:
                self.delta.x = dx / (dist / 100)
                self.delta.y = dy / (dist / 100)
            else:
                self.delta.x = 0
                self.delta.y = 0

        self.last_cursor_pos = pg.Vector2(pg.mouse.get_pos())
        
        # Centraliza o cursor na tela
        if not (50 < self.last_cursor_pos.x < DW - 50) or not (50 < self.last_cursor_pos.y < DH - 50):
            pg.mouse.set_pos(DW / 2, DH / 2)
            self.last_cursor_pos = pg.Vector2(DW / 2, DH / 2)
