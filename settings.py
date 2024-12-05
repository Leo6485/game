import pygame as pg

# Tela
pg.init()
d = pg.display.Info()
DW, DH = d.current_w, d.current_h
del d

# Cores
GREEN = (0, 255, 0)
GRID_COLOR = (0, 0, 0)
BG_COLOR = (20, 20, 20)
FINAL_BG_COLOR = (0, 0, 0)

# FPS
FPS = 60