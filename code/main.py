import pygame
import math
import time
import random
import copy
from bases.colors import COLORS
from bases.board import BOARD
import bases.essence as ESSENCES


class LOOP():

    def __init__(self, src, disabler, flipper, fps=30):
        self.screen = src
        self.width, self.height = self.screen.get_size()
        self.squareSize = min(self.width / 5 * 4, self.height - 10)
        self.disableEvent = disabler
        self.flipEvent = flipper
        self.fps = fps
        self.timer = pygame.time.Clock()
        self.timer.tick(self.fps)

        self.btnsSurf = pygame.Surface((max(self.squareSize / 4, 20) - 5, (self.height -
                                                                           self.squareSize) / 2 + self.squareSize / 4 * 3 + 12 - (self.height) / 5))
        self.btnsSurfPos = (
            self.width - max(self.squareSize / 4, 20), (self.height) / 5)

        self.textSurfPos = ((self.width - self.squareSize) / 2,
                            (self.height - self.squareSize) / 2 + self.squareSize / 4 * 3 + 12)
        self.textSurf = pygame.Surface(
            (self.squareSize, int(self.squareSize / 4) - 20))
        # Colors
        self.BLACK = COLORS.BLACK
        self.PURPLE = COLORS.PURPLE

        # create standart events
        self.quit = pygame.QUIT
        self.keyDown = pygame.KEYDOWN
        self.keyUp = pygame.KEYUP
        self.moseMoved = pygame.MOUSEMOTION
        self.mouseUp = pygame.MOUSEBUTTONUP
        self.mouseDown = pygame.MOUSEBUTTONDOWN
        self.sizeChanged = pygame.VIDEORESIZE

        # some need things
        self.last = 274
        self.bullets = []
        self.timers = {}
        self.opacity = 200

    def createNewTimer(self, eventName, thisTime, event):
        pygame.time.set_timer(eventName, int(thisTime))
        self.timers[eventName] = (thisTime, event)

    def reloadBulletsPoses(self):
        pass

    def render(self):
        self.screen.fill(self.BLACK)

        self.textSurf.fill(self.BLACK)
        self.textSurf.set_alpha(self.opacity)
        self.btnsSurf.fill(self.PURPLE)
        self.btnsSurf.set_alpha(self.opacity / 2)

        self.board.renderCells(
            self.screen, xMax=self.width, pos2=self.boardSize)

        #self.screen.blit(self.textSurf, self.textSurfPos)
        #self.screen.blit(self.btnsSurf, self.btnsSurfPos)

        self.flipEvent()

    def reloadSize(self, event):
        event.dict['size'] = max(event.dict['size'][0], 720), max(
            event.dict['size'][1], 360)
        self.screen = pygame.display.set_mode(
            event.dict['size'], pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.squareSize = min(self.width / 5 * 4, self.height - 10)

        self.boardSizer()

        self.textSurf = pygame.Surface(
            (self.squareSize, int(self.squareSize / 4) - 20))
        self.textSurfPos = ((self.width - self.squareSize) / 2,
                            (self.height - self.squareSize) / 2 + self.squareSize / 4 * 3 + 12)

        self.btnsSurf = pygame.Surface((max(self.squareSize / 4, 20) - 5, (self.height -
                                                                           self.squareSize) / 2 + self.squareSize / 4 * 3 + 12 - (self.height) / 5))
        self.btnsSurfPos = (
            self.width - max(self.squareSize / 4, 20), (self.height) / 5)

    def boardSizer(self, x=30, y=15):
        self.boardSize = (x, y)
        self.board.autoSizer(self.width, self.height, x, y)
        self.board.resizeEssences()

    def create(self, thisDisabler=None, thisFlipper=None):
        pygame.NUMEVENTS += 100
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper
        pygame.init()
        pygame.mouse.set_visible(False)
        self.width, self.height = self.screen.get_size()

        self.board = BOARD(40, 40, rules={"deep": 4})
        self.boardSizer()
        print("\n".join(list(map(lambda x: " ".join(list(map(lambda y: "{:3d}".format(int(y)), x))), self.board.cells))))

        #self.player = PLAYER(0, 0, "data/player")

        self.testDecor = ESSENCES.STATIC_DECORATION(
            1, 1, folder="data/essences/decore/", texturename="redWallFire.png")
        self.board.insertStaticEssence(self.testDecor)

        self.createNewTimer(30, 1 / self.fps * 1000, lambda: self.render())
        # main Loop
        while 1:
            for Event in pygame.event.get():
                t = Event.type
                if t == self.sizeChanged:
                    self.reloadSize(Event)
                if t == self.quit:
                    self.disableEvent()
                    return
                if t in self.timers:
                    self.timers[t][1]()


if __name__ == '__main__':
    screen = pygame.display.set_mode((720, 360), pygame.RESIZABLE)
    loop = LOOP(screen, pygame.quit, pygame.display.flip)
    loop.create()
