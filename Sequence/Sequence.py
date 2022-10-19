import pygame as pg
import random
import time

pg.init()

MAPSIZE = 3
SPEED = 0.4
SCREENSIZE = 700

SHOWN = (140, 140, 220)
CLICKED = (220, 140, 140)
EMPTY = (170,170,170)
BACKGROUND = (255,255,255)
FONT = pg.font.SysFont("timesnewroman.ttf", 72)
TEXT = (20, 20, 20)

class Game:

    def __init__(self, mapsize = 3, speed = 0.75, screensize = 700):
        self.screen = pg.display.set_mode((screensize, screensize))
        self.screensize = screensize
        self.score = 0 
        self.mapsize = mapsize # 3x3, can be 2 for 2x2 or 4 for 4x4 etc.
        self.speed = speed # in seconds, how long it takes between shown boxes in the View state
        self.boxes = [] # list of boxes to click on in order for example [0,3,2,2,1,3] each item must be between 0 and mapsize**2 - 1 included
        self.state = "End" #View, Play, End
        self.index = 0 # current box index, self.boxes[self.index] being the current box youre supposed to click on
        self.clickedbox = None # the box you clicked on
        self.shownbox = None # the box currently shown in view state
    
    def boxtopos(self, box):
        return (box % self.mapsize, box // self.mapsize)
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # in 3x3, 3 -> (0, 1)
        # in 2x2, 3 -> (1, 1)
        # in 3x3, 4 -> (1, 1)

    def postobox(self, pos):
        '''inverse of boxtopos'''
        x, y = pos
        return x + y * self.mapsize
        # in any mapsize, (0,0) -> 0
        # in 3x3, (1,1) -> 4
        # in 2x2, (1,1) -> 3
        # in 5x5, (4,4) -> 24
    
    def addbox(self):
        self.boxes.append(random.randint(0, self.mapsize**2 - 1))

    def update(self):
        self.screen.fill(EMPTY)
        for box in range(self.mapsize**2):
            if box == self.clickedbox:
                pg.draw.rect(self.screen, CLICKED, (box % self.mapsize * self.screensize//self.mapsize, box // self.mapsize * self.screensize//self.mapsize, self.screensize//self.mapsize, self.screensize//self.mapsize))
            elif box == self.shownbox:
                pg.draw.rect(self.screen, SHOWN, (box % self.mapsize * self.screensize//self.mapsize, box // self.mapsize * self.screensize//self.mapsize, self.screensize//self.mapsize, self.screensize//self.mapsize))
        pg.display.update()

    def mousepostobox(self, pos):
        x, y = pos
        if x > self.screensize or y > self.screensize:
            return None
        return self.postobox((x // (self.screensize//self.mapsize), y // (self.screensize//self.mapsize)))
    
    def play(self):
        self.update()
        time.sleep(self.speed)
        while self.state != "End":
            self.addbox()
            for box in self.boxes:
                self.shownbox = box
                self.update()
                time.sleep(self.speed*3/4)
                self.shownbox = None
                self.update()
                time.sleep(self.speed/4)
            self.state = "Play"
            self.index = 0
            while self.state == "Play":
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if self.mousepostobox(pg.mouse.get_pos()) != None:
                            self.clickedbox = self.mousepostobox(pg.mouse.get_pos())
                            self.update()
                            time.sleep(self.speed/4)
                            if self.boxes[self.index] == self.clickedbox:
                                self.index += 1
                                self.clickedbox = None
                                self.update()
                                if self.index == len(self.boxes):
                                    self.score += 1
                                    time.sleep(self.speed)
                                    self.state = "View"
                            else:
                                self.shownbox = self.boxes[self.index]
                                self.update()
                                time.sleep(self.speed*2)
                                self.shownbox = None
                                self.clickedbox = None
                                self.state = "End"

    def menu(self):
        self.screen.fill(BACKGROUND)
        pressspace = FONT.render("Press space to play", True, TEXT)
        scorecount = FONT.render(f'Score: {self.score}', True, TEXT)
        self.screen.blit(scorecount, (10, 10))
        self.screen.blit(pressspace, (10, 10 + pressspace.get_height()))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = "View"
                self.score = 0
                self.boxes = []

    def run(self):
        while True:
            if self.state == "View" or self.state == "Play":
                self.play()
            elif self.state == "End":
                self.menu()

def main():
    game = Game(MAPSIZE, SPEED, SCREENSIZE)
    game.run()


if __name__ == "__main__":
    main()
