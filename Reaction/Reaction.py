import numpy as np
import random
import time
import pygame as pg


pg.init()

WAIT = (220, 100, 100)
CLICK = (100, 220, 100)
BACKGROUND = (150, 150, 150)
font = pg.font.SysFont('timesnewroman.ttf', 72)
TEXT = (20, 20, 20)



class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((700, 700))
        self.screen.fill(BACKGROUND)
        self.state = "Idle" # Idle, Wait, Click
        self.timelist = [] # List of reaction times
        self.start = time.time()

    def render(self):
        if self.state == "Idle":
            self.screen.fill(BACKGROUND)
            spacestart = font.render("Press Space to Start", 1, TEXT)
            self.screen.blit(spacestart, (10, 50))
            if len(self.timelist) > 0:
                average = font.render("Tries: %d" %len(self.timelist), 1, TEXT)
                count = font.render("Average: %d ms" %int(np.mean(self.timelist)), 1, TEXT)
                last = font.render("%d ms" %self.timelist[-1], 1, TEXT)
                self.screen.blit(last, (200, 250))
                self.screen.blit(average, (200, 350))
                self.screen.blit(count, (200, 400))
        elif self.state == "Wait":
            self.screen.fill(WAIT)
            wait = font.render("Wait...", 1, TEXT)
            self.screen.blit(wait, (50, 50))
        elif self.state == "Click":
            self.screen.fill(CLICK)
            click = font.render("Click!", 1, TEXT)
            self.screen.blit(click, (50, 50))
        pg.display.update()

    def run(self):
        i = 0
        rand = (random.random()*4 + 2)*100
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if self.state == "Idle":
                            self.state = "Wait"
                            self.render()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.state == "Click":
                        self.timelist.append(abs(int((time.time() - self.start)*1000) - 35)) #-35 ms to approximately account for the delay caused by the program itself
                        self.state = "Idle"
                        i = 0
                        rand = (random.random()*4 + 2)*100
            self.render()
            time.sleep(0.01)
            if self.state == "Wait":
                if i < rand:
                    i += 1
                else:
                    self.state = "Click"
                    self.start = time.time()

if __name__ == "__main__":
    game = Game()
    game.run()
    




