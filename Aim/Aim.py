import pygame as pg
import random
import time
import numpy as np

pg.init()

SIZE = 100
HEIGHT = 700
WIDTH = 1000
BOXCOUNT = 15
SPEED = 0.5

SHOWN = (140, 140, 220)
EMPTY = (170,170,170)
BACKGROUND = (255,255,255)
FONT = pg.font.SysFont("timesnewroman.ttf", 72)
TEXT = (20, 20, 20)

class Game:

    def __init__(self, size = 50, screenheight = 700, screenwidth = 1000, boxcount = 20, speed = 0.5):
        self.screen = pg.display.set_mode((screenwidth, screenheight))
        self.screenheight = screenheight
        self.screenwidth = screenwidth
        self.speed = speed
        self.boxcount = boxcount
        self.box = None # position of the current box, ex: (230, 473), becomes None when the game is over
        self.size = size # in pixels, how big the boxes are
        self.times = [] # list of milliseconds between hits
        self.lastclick = 0
        self.state = "End" #Play, End
    
    def placebox(self):
        self.box = (random.randint(self.size, self.screenwidth - self.size), random.randint(self.size, self.screenheight - self.size))

    def update(self):
        self.screen.fill(EMPTY)
        if self.box:
            pg.draw.rect(self.screen, SHOWN, (self.box[0], self.box[1], self.size, self.size))
        pg.display.update()

    def isinbox(self, pos):
        x, y = pos
        if x > self.box[0] and x < self.box[0] + self.size and y > self.box[1] and y < self.box[1] + self.size:
            return True
        return False
    
    def play(self):
        self.update()
        time.sleep(self.speed)
        while self.state != "End":
            self.placebox()
            self.update()
            self.lastclick = time.time()
            while self.box:
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if self.isinbox(pg.mouse.get_pos()):
                            self.box = None
                            self.times.append(time.time() - self.lastclick)
                            self.lastclick = self.times[-1]
                            self.update()
                            if len(self.times) == self.boxcount:
                                time.sleep(self.speed)
                                self.state = "End"

    def menu(self):
        self.screen.fill(BACKGROUND)
        pressspace = FONT.render("Press space to play", True, TEXT)
        if len(self.times):
            scorecount = FONT.render(f'Average time between hits: {int(round(np.mean(self.times), 4)*1000)} ms', True, TEXT)
            self.screen.blit(scorecount, (10, 10))
        self.screen.blit(pressspace, (10, 10 + pressspace.get_height()))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = "Play"
                self.box = None
                self.times = []

    def run(self):
        while True:
            if self.state == "Play":
                self.play()
            elif self.state == "End":
                self.menu()

def main():
    game = Game(SIZE, HEIGHT, WIDTH, BOXCOUNT, SPEED)
    game.run()


if __name__ == "__main__":
    main()
