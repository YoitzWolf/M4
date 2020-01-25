import pygame
import math
import time
import random
import copy

import bases.interfaces as INTERFACE
from bases.colors import COLORS


class ESSENCE(pygame.sprite.Sprite):

    def __init__(self, x, y, filename):
        super(ESSENCE, self).__init__()
        self.x = x
        self.y = y
        self.defaultImage = filename
        
       
    def render(self, screen):
        if self.size != 32:
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        screen.blit(self.image, self.rect)

    def setSize(self, size=32):
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = int(4/32 * self.size)


class BULLET(ESSENCE):

    def __init__(self, parent, pos, filename="data/essences/bulletForward.png"):
        self.parent = parent
        self.speed = 1
        super(BULLET, self).__init__(parent.x, parent.y, filename)


class PLAYER(ESSENCE, INTERFACE.STATIC_VECTOR, INTERFACE.MOVE_ANIMATED):

    def __init__(self, x, y, filename):
        ESSENCE.__init__(self, x, y, filename)
        self.forward = [274, 115]
        self.back = [273, 119]
        self.right = [275, 100]
        self.left = [276, 97]
