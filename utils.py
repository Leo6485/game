import pygame as pg 

def draw_grid(surface, color, cell_size):
    width, height = surface.get_size()
    for x in range(0, width, cell_size):
        pg.draw.line(surface, color, (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pg.draw.line(surface, color, (0, y), (width, y))