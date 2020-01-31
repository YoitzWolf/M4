import pygame
import math
import time
import random
import copy

import bases.interfaces as INTERFACE
from bases.colors import COLORS


class ESSENCE(pygame.sprite.Sprite, INTERFACE.IMAGE_LOADER):

    def __init__(self, x, y, folder):
        super(ESSENCE, self).__init__()
        self.x = x
        self.y = y
        self.folder = folder
        self.size = 32
        
       
    def render(self, screen):
        screen.blit(self.image, self.rect)

    def setSize(self, size=32):
        old = self.size
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        if isinstance(self, INTERFACE.MOVEABLE):
            self.speed = int(self.rawSpeed/old * self.size)

    def setPos(self, size=32):
        old = self.size
        self.rect.x = self.x * size
        self.rect.y = self.y * size

class STATIC_DECORATION(ESSENCE):

    def __init__(self, x, y, folder, texturename):
        ESSENCE.__init__(self, x, y, folder)
        self.texturename = texturename
        self.load()
        
class BULLET(ESSENCE, INTERFACE.MOVE_ANIMATED):

    def __init__(self, parent, vector, speed=1, folder="data/essences/bullet/"):
        self.parent = parent
        self.speed = speed
        self.rawSpeed = speed
        super(BULLET, self).__init__(parent.x, parent.y, folder)


class PLAYER(ESSENCE, INTERFACE.STATIC_VECTOR, INTERFACE.MOVE_ANIMATED):

    def __init__(self, x, y, filename):
        ESSENCE.__init__(self, x, y, filename)
        self.forward = [274, 115]
        self.back = [273, 119]
        self.right = [275, 100]
        self.left = [276, 97]
