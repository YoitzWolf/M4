import pygame
import math
import time
import random
import copy
from bases.colors import COLORS
from bases.board import BOARD
import bases.essence as ESSENCES
from bases.camera import CAMERA


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

    def reloadPoses(self):
        self.camera.selectedModelPosManager()

    def render(self):
        self.screen.fill(self.BLACK)

        self.textSurf.fill(self.BLACK)
        self.textSurf.set_alpha(self.opacity)
        self.btnsSurf.fill(self.PURPLE)
        self.btnsSurf.set_alpha(self.opacity / 2)
        # board.renderCells(self.screen, xMax=self.width, pos2=self.boardSize)
        self.camera.render(self.screen, self.width)

        self.screen.blit(self.textSurf, self.textSurfPos)
        #self.screen.blit(self.btnsSurf, self.btnsSurfPos)

        self.flipEvent()

    def reloadSize(self, event):
        event.dict['size'] = max(event.dict['size'][0], 720), max(
            event.dict['size'][1], 360)
        self.screen = pygame.display.set_mode(
            event.dict['size'], pygame.RESIZABLE)
        self.width, self.height = self.screen.get_size()
        self.squareSize = min(self.width / 5 * 4, self.height - 10)

        self.camera.boardSizer(self.width, self.height)

        self.textSurf = pygame.Surface(
            (self.squareSize, int(self.squareSize / 4) - 20))
        self.textSurfPos = ((self.width - self.squareSize) / 2,
                            (self.height - self.squareSize) / 2 + self.squareSize / 4 * 3 + 12)

        # self.btnsSurf = pygame.Surface((max(self.squareSize / 4, 20) - 5, (self.height -
        #                                                                   self.squareSize) / 2 + self.squareSize / 4 * 3 + 12 - (self.height) / 5))
        # self.btnsSurfPos = (
        #    self.width - max(self.squareSize / 4, 20), (self.height) / 5)

    def create(self, thisDisabler=None, thisFlipper=None):
        pygame.NUMEVENTS += 100
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper
        pygame.init()
        pygame.mouse.set_visible(False)
        self.width, self.height = self.screen.get_size()

        self.camera = CAMERA(2, 2)

        board = BOARD(40, 40, rules={"deep": 4})
        self.camera.setCameraBoard(board)
        self.camera.boardSizer(self.width, self.height)

        player = ESSENCES.PLAYER(self.camera.board.cellSize * 2,
                                 self.camera.board.cellSize * 2, "data/essences/player")

        staticImages = ["/staticRight.png", "/staticBack.png","/staticLeft.png", "/staticForward.png"]
        movingImages = [["/goRight0.png", "/goRight1.png"], ["/goBack0.png", "/goBack1.png"], ["/goLeft0.png", "/goLeft1.png"], ["/goForward0.png", "/goForward1.png"]]

        player.staticImagesInit(staticImages)
        player.moveImagesInit(movingImages)

        player.changeStaticTexture(0, 0)
        player.load()

        self.camera.setCameraSelection(player)
        # print("\n".join(list(map(lambda x: " ".join(list(map(lambda y:
        # "{:3d}".format(int(y)), x))), self.board.cells)))) #map logging

        #

        
        self.createNewTimer(31, 1 / self.fps * 4000, lambda: self.reloadPoses())
        self.createNewTimer(30, 1 / self.fps * 1000, lambda: self.render())
        # main Loop
        self.render()
        while 1:
            for Event in pygame.event.get():
                t = Event.type
                if t == self.sizeChanged:
                    self.reloadSize(Event)
                if t == self.keyDown or t == self.keyUp:
                    self.camera.keysInterpretator(
                        Event.key, (t == self.keyDown))
                if t == self.quit:
                    self.disableEvent()
                    return
                if t in self.timers:
                    self.timers[t][1]()


if __name__ == '__main__':
    screen = pygame.display.set_mode((720, 360), pygame.RESIZABLE)
    loop = LOOP(screen, pygame.quit, pygame.display.flip)
    loop.create()
