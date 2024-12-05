import pygame as pg
from game import Game

def main():
    pg.init()
    pg.display.set_caption("Jogo")
    pg.mouse.set_visible(False)

    game = Game()
    game.run()

    pg.quit()


if __name__ == "__main__":
    main()
