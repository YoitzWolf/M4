import pygame
import math
import time
import random
import copy
from bases.board import BOARD
from bases.essence import PLAYER
from bases.essence import BULLET


class LOOP():

    def __init__(self, src, disabler, flipper, fps=30):
        self.screen = src
        self.disableEvent = disabler
        self.flipEvent = flipper
        self.fps = fps
        self.timer = pygame.time.Clock()
        self.timer.tick(self.fps)
        self.quit = pygame.QUIT
        self.keyDown = pygame.KEYDOWN
        self.keyUp = pygame.KEYUP
        self.moseMoved = pygame.MOUSEMOTION
        self.mouseUp = pygame.MOUSEBUTTONUP
        self.mouseDown = pygame.MOUSEBUTTONDOWN
        self.bullets = []
        self.timers = {}
        self.names = set()

    def createNewTimer(self, eventName, thisTime, event):
        pygame.time.set_timer(eventName, int(thisTime))
        self.timers[eventName] = (thisTime, event)
        self.names.add(eventName)

    def reloadBulletsPoses(self):
        for bullet in self.bullets:
            if bullet.pos == 0:
                bullet.y += bullet.speed
                bullet.rect.y += bullet.speed
            elif bullet.pos == 1:
                bullet.x += bullet.speed
                bullet.rect.x += bullet.speed
            elif bullet.pos == 2:
                bullet.x -= bullet.speed
                bullet.rect.x -= bullet.speed
            elif bullet.pos == 3:
                bullet.y -= bullet.speed
                bullet.rect.y -= bullet.speed

    def render(self):
        self.reloadBulletsPoses()
        self.screen.fill((50, 50, 50))
        self.player.paint(self.screen)
        for i in self.bullets:
            i.paint(self.screen)
        self.flipEvent()

    def shootEvent(self):
        if self.player.shootPos == 2:
            self.createNewTimer(31, -1, lambda: False)
            # here create bullet
            bullet = BULLET(self.player, self.last)
            bullet.initImages(self.last)
            bullet.setSize(size=64)
            self.bullets.append(bullet)
            self.player.staticEvent(self.last)
        elif self.player.shootPos == 0 or self.player.shootPos == 1:
            self.player.fightEvent(self.last)

    def create(self, thisDisabler=None, thisFlipper=None):
        if thisDisabler is not None:
            self.disableEvent = thisDisabler
        if thisFlipper is not None:
            self.flipEvent = thisFlipper
        pygame.init()
        self.last = 274
        self.player = PLAYER(250, 250, "data/player/staticForward.png")
        self.player.setSize(size=64)
        self.player.initImages()

        self.createNewTimer(30, 1 / self.fps * 1000, lambda: self.render())
        self.createNewTimer(29, 1 / self.fps * 100, lambda: self.reloadBulletsPoses())
        # main Loop
        while 1:
            for Event in pygame.event.get():
                t = Event.type
                if t == self.keyDown:
                    if self.player.correctMovementKey(Event.key):
                        self.player.staticEvent(Event.key)
                        self.last = Event.key
                        self.createNewTimer(31, 150, lambda: self.player.move(self.last))

                if t == self.keyUp and Event.key != 102 and Event.key == self.last:
                    self.player.staticEvent(self.last)
                    self.createNewTimer(31, -1, lambda: False)

                if t == self.mouseDown and Event.button == 1 and self.player.shootPos == 0:
                    self.player.staticEvent(self.last)
                    self.player.fightLvl = 0
                    self.createNewTimer(31, 150, self.shootEvent)
                elif t == self.keyDown and Event.key == 102 and self.player.shootPos == 0:
                    self.player.staticEvent(self.last)
                    self.player.fightLvl = 0
                    self.createNewTimer(31, 150, self.shootEvent)

                if t == self.quit:
                    self.disableEvent()
                    return
                if t in self.timers:
                    self.timers[t][1]()

screen = pygame.display.set_mode((520, 520))
loop = LOOP(screen, pygame.quit, pygame.display.flip)
loop.create()
