import pygame
import math
import time
import random
import copy

import classes.interfaces as INTERFACE
from classes.colors import COLORS


class BACKGROUND_IMAGE(INTERFACE.DRAWABLE_PER_COORDS):

    def __init__(self, folder, texturename):
        self.x = 0
        self.y = 0
        self.folder = folder
        self.texturename = texturename
        self.width = 0
        self.height = 0
        self.rawSpeed = 0

    def load(self):
        self.image = pygame.image.load(
            self.folder + self.texturename).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    def resize(self):
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def setSize(self, w, h):
        self.width = w
        self.height = h
        self.resize()


class BACK_SPRITE_UNIT(INTERFACE.DRAWABLE_PER_COORDS):

    def __init__(self, size, name=None, color=COLORS.BLACK, helpColor=COLORS.WHITE, rand=80):
        self.width = 1
        self.height = 1
        self.size = size
        self.cell = size
        self.color = color
        self.helpColor = helpColor
        self.texturename = None
        self.foldername = None
        self.image = None
        if name is not None and random.randint(0, 100) > rand:
            self.texturename = name[1]
            self.folder = name[0]
            self.load()

    def resize(self, size):
        if self.texturename is not None:
            self.setSize(cell=size)
        self.size = size

    def render(self, surf, x, y):
        #pygame.draw.rect(surf, self.color, (x, y, self.size, self.size))
        #pygame.draw.rect(surf, self.helpColor, (x, y, self.size, self.size), 1)
        if self.image is not None:
            self.draw_per_coords(surf, x, y)


class ESSENCE(pygame.sprite.Sprite, INTERFACE.DRAWABLE):

    def __init__(self, x, y, folder):
        super(ESSENCE, self).__init__()
        self.x = x
        self.y = y
        self.folder = folder
        self.width = 1
        self.height = 1
        self.cell = 32  # cell size
        self.rawSpeed = 0

    def setLayout(self, surf):
        self.surface = surf

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x * self.cell
        self.rect.y = self.y * self.cell

    def delta(self, tick):
        return self.rawSpeed * tick / 100


class BULLET(ESSENCE, INTERFACE.MOVEABLE, INTERFACE.CROSSABLE, INTERFACE.STATIC_FRAME):

    def __init__(self, parent, x, y, cell, vector=0, speed=0.7, folder="data/bg/bullet"):
        super(BULLET, self).__init__(x, y, folder)
        self.parent = parent
        self.rawSpeed = speed
        self.cell = cell
        self.staticImagesInit(
            ['/bullet_1.png', '/bullet_0.png', '/bullet_0.png', '/bullet_1.png'])
        self.texturename = '/bullet_0.png'


class PLAYER(ESSENCE, INTERFACE.STATIC_FRAME, INTERFACE.CONTROLLED, INTERFACE.SHOOTING, INTERFACE.KILLABLE, INTERFACE.VECTORMOVEABLE):

    def __init__(self, x, y, folder):
        self.setHP(1000)
        self.initVector(radialSpeed=0.03)
        ESSENCE.__init__(self, x, y, folder)
        self.initControlKeys({
            "forward": [119, 273],
            "back": [115, 274],
            "right": [],  # [275, 100],
            "left": []  # [276, 97]
        })
        self.shootInit()
        self.rawSpeed = 0.5


class BASTARD(ESSENCE, INTERFACE.STATIC_FRAME, INTERFACE.SHOOTING, INTERFACE.CROSSABLE, INTERFACE.KILLABLE, INTERFACE.MOVEABLE):

    def __init__(self, x, y, folder):
        self.moveableInit()
        self.setHP(10)
        ESSENCE.__init__(self, x, y, folder)
        self.shootInit()
        self.rawSpeed = 0.25

        self.staticImagesInit(
            ['/bastard_1.png', '/bastard_0.png', '/bastard_0.png', '/bastard_1.png'])
        self.texturename = '/bastard_0.png'
