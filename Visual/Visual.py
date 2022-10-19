import pygame as pg
import random
import time

pg.init()

SPEED = 0.5
SCREENSIZE = 700

SHOWN = (140, 140, 220)
CLICKED = (220, 140, 140)
SHLICKED = (170, 140, 170)
EMPTY = (170,170,170)
BACKGROUND = (255,255,255)
FONT = pg.font.SysFont("timesnewroman.ttf", 72)
TEXT = (20, 20, 20)

class Game:
    def __init__(self, speed = 0.5, screensize = 700):
        self.speed = speed
        self.screen = pg.display.set_mode((screensize, screensize))
        self.screensize = screensize
        self.score = 0
        self.state = "End" #View, Play, End
        self.boxes = set() #List of boxes youre supposed to click on
        self.shownboxes = set() #List of boxes that are shown
        self.clickedboxes = set() #List of boxes you clicked on
        self.currentmapsize = 3 # + 1 when (self.score + 1) / self.currentmapsize**2 > 0.45

    def boxtopos(self, box):
        return (box % self.currentmapsize, box // self.currentmapsize)
    
    def postobox(self, pos):
        x, y = pos
        return x + y * self.currentmapsize
    
    def generate_boxlist(self):
        self.boxes = set()
        while len(self.boxes) < self.score + 1:
            self.boxes.add(random.randint(0, self.currentmapsize**2 - 1))
        
    def update(self):
        self.screen.fill(EMPTY)
        for box in range(self.currentmapsize**2):
            if box in self.shownboxes:
                if box in self.clickedboxes:
                    pg.draw.rect(self.screen, SHLICKED, (box % self.currentmapsize * self.screensize//self.currentmapsize, box // self.currentmapsize * self.screensize//self.currentmapsize, self.screensize//self.currentmapsize, self.screensize//self.currentmapsize))
                else:
                    pg.draw.rect(self.screen, SHOWN, (box % self.currentmapsize * self.screensize//self.currentmapsize, box // self.currentmapsize * self.screensize//self.currentmapsize, self.screensize//self.currentmapsize, self.screensize//self.currentmapsize))
            elif box in self.clickedboxes:
                pg.draw.rect(self.screen, CLICKED, (box % self.currentmapsize * self.screensize//self.currentmapsize, box // self.currentmapsize * self.screensize//self.currentmapsize, self.screensize//self.currentmapsize, self.screensize//self.currentmapsize))
        pg.display.update()

    def mousepostobox(self, pos):
        x, y = pos
        if x > self.screensize or x < 0 or y < 0 or y > self.screensize:
            return None
        return self.postobox((x // (self.screensize//self.currentmapsize), y // (self.screensize//self.currentmapsize)))

    def play(self):
        self.score = 0
        while self.state != "End":
            self.shownboxes = set()
            self.clickedboxes = set()
            self.update()
            time.sleep(self.speed/2)
            self.generate_boxlist()
            self.update()
            time.sleep(self.speed/2)
            self.shownboxes = self.boxes.copy()
            self.update()
            self.state = "Play"
            time.sleep(self.speed)
            self.shownboxes = set()
            self.update()
            while self.state == "Play":
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        lastclick = self.mousepostobox(pg.mouse.get_pos())
                        if lastclick != None:
                            self.clickedboxes.add(lastclick)
                            self.update()
                            if lastclick in self.boxes:
                                if len(self.clickedboxes) == len(self.boxes):
                                    self.score += 1
                                    if self.score >= self.currentmapsize**2*0.45:
                                        self.currentmapsize += 1
                                    self.state = "View"
                                    time.sleep(self.speed/2)
                                    self.clickedboxes = set()
                                    self.update()
                                    time.sleep(self.speed/2)
                            else:
                                self.shownboxes = self.boxes.copy()
                                self.update()
                                time.sleep(self.speed*2)
                                self.state = "End"
                                self.currentmapsize = 3
                    pg.event.clear(pg.MOUSEBUTTONDOWN)

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

    def run(self):
        while True:
            if self.state == "View" or self.state == "Play":
                self.play()
            elif self.state == "End":
                self.menu()
                

def main():
    game = Game(SPEED, SCREENSIZE)
    game.run()


if __name__ == "__main__":
    main()
