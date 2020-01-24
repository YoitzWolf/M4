import pygame
import math
import time
import random
import copy


class ESSENCE(pygame.sprite.Sprite):

    def __init__(self, x, y, filename):
        super(ESSENCE, self).__init__()
        self.x = x
        self.y = y
        self.defaultImage = filename
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.size = 32
        self.staticImages = {}
        self.moveImages = {}
        self.fightImages = {}
        self.speed = 4
        self.shootPos = 0

        self.forward = [274, 115]
        self.back = [273, 119]
        self.right = [275, 100]
        self.left = [276, 97]

    def paint(self, screen):
        if self.size != 32:
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        screen.blit(self.image, self.rect)

    def addStaticImage(self, key, image):
        self.staticImages[key] = image

    def addMoveImage(self, key, image):
        self.moveImages[key] = image

    def addFightImage(self, key, image):
        self.fightImages[key] = image

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

    def setImage(self, src):
        self.image = pygame.image.load(src).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def setSize(self, size=32):
        self.size = size
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = self.size/32

    def initImages(self, i):
        if i in self.parent.forward:
            self.pos = 0
            self.setImage("data/essences/bulletForward.png")
        elif i in self.parent.right:
            self.pos = 1
            self.setImage("data/essences/bulletRight.png")
        elif i in self.parent.left:
            self.pos = 2
            self.setImage("data/essences/bulletLeft.png")
        elif i in self.parent.back:
            self.pos = 3
            self.setImage("data/essences/bulletBack.png")


class PLAYER(ESSENCE):

    def __init__(self, x, y, filename):
        super(PLAYER, self).__init__(x, y, filename)
        self.movements = self.forward + self.back + self.right + self.left

    def correctMovementKey(self, key):
        return key in self.movements

    def initImages(self):
        for i in self.forward:
            self.addStaticImage(i, "data/player/staticForward.png")
            self.addMoveImage((i, 0), "data/player/goForward0.png")
            self.addMoveImage((i, 1), "data/player/goForward1.png")
            self.addFightImage((i, 0), "data/player/shootForward0.png")
            self.addFightImage((i, 1), "data/player/shootForward1.png")

        for i in self.right:
            self.addStaticImage(i, "data/player/staticRight.png")
            self.addMoveImage((i, 0), "data/player/goRight0.png")
            self.addMoveImage((i, 1), "data/player/goRight1.png")
            self.addFightImage((i, 0), "data/player/shootRight0.png")
            self.addFightImage((i, 1), "data/player/shootRight1.png")

        for i in self.left:
            self.addStaticImage(i, "data/player/staticLeft.png")
            self.addMoveImage((i, 0), "data/player/goLeft0.png")
            self.addMoveImage((i, 1), "data/player/goLeft1.png")
            self.addFightImage((i, 0), "data/player/shootLeft0.png")
            self.addFightImage((i, 1), "data/player/shootLeft1.png")

        for i in self.back:
            self.addStaticImage(i, "data/player/staticBack.png")
            self.addMoveImage((i, 0), "data/player/goBack0.png")
            self.addMoveImage((i, 1), "data/player/goBack1.png")
            self.addFightImage((i, 0), "data/player/shootBack0.png")
            self.addFightImage((i, 1), "data/player/shootBack1.png")

    def staticEvent(self, key):
        try:
            self.pos = -1
            self.shootPos = 0
            self.image = pygame.image.load(self.staticImages[key])
            pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        except Exception as e:
            print(e)

    def fightEvent(self, key):
        try:
            self.image = pygame.image.load(
                self.fightImages[(key, self.shootPos)])
            pygame.transform.scale(self.image, (self.size, self.size))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.shootPos += 1
        except Exception as e:
            print(e)

    def move(self, key):
        if key in self.forward + self.back + self.right + self.left:
            if key in self.forward:
                self.rect.y += self.speed
                self.y += self.speed
            elif key in self.back:
                self.rect.y -= self.speed
                self.y -= self.speed
            elif key in self.left:
                self.rect.x -= self.speed
                self.x -= self.speed
            elif key in self.right:
                self.rect.x += self.speed
                self.x += self.speed
            self.pos += 1
            self.pos %= 2
            self.image = pygame.image.load(self.moveImages[(key, self.pos)])
