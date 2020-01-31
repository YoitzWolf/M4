import pygame
import math
import time
import random
import copy

import bases.essence as ESSENCES
from bases.colors import COLORS
import bases.interfaces as INTERFACE


class BOARD():

    def __init__(self, width, height, rules={}):
        self.width = width
        self.height = height
        self.cellSize = None
        self.BLACK = COLORS.BLACK
        self.x = 0
        self.y = 0
        self.roomSize = (width, height)
        self.cells = INTERFACE.DANGEON_MANAGER.manager(width, height, rules)
        self.surface = pygame.Surface([1, 1])
        self.colors = [COLORS.BLACK, COLORS.GRAY]
        self.essences = {}
        self.staticEssences = []

    def insertEssence(self, essence, program):
        if isinstance(essence, ESSENCES.ESSENCE) and isinstance(essence, INTERFACE.MOVEABLE):
            self.essences.append([essence, program])

    def insertStaticEssence(self, essence):
        if isinstance(essence, ESSENCES.ESSENCE):
            print(self.cellSize)
            essence.setSize(size=self.cellSize)
            essence.setPos(size=self.cellSize)
            self.staticEssences.append(essence)
    
    def setCoords(self, x, y):
        self.x = x
        self.y = y

    def resize(self, x, y):
        self.width = x
        self.height = y
        newCells = [[0] * self.width for i in range(self.height)]
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                newCells[i][j] = self.cells[i][j]
        self.cells = newCells

    def get_cell(self, pos):
        x = pos[0] - self.x
        y = pos[1] - self.y
        if x < 0 or y < 0:
            return None
        if x > self.width * self.cellSize or y > self.height * self.cellSize:
            return None
        resX = x // self.cellSize
        resY = y // self.cellSize
        return resX, resY

    def resizeEssences(self):
        for item in range(len(self.staticEssences)):
            self.staticEssences[item].load()
            self.staticEssences[item].setSize(size=self.cellSize)
            self.staticEssences[item].setPos(size=self.cellSize)

    def on_click(self, cell):
        pass

    def click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def autoSizer(self, width, height, cellCountX, cellCountY):
        self.cellSize = int(min(width / cellCountX, height / cellCountY))
        self.surface = pygame.Surface([cellCountX * self.cellSize, cellCountY * self.cellSize])

    def renderStaticEssenses(self, screen, fromPos=(0, 0), toPos=None):
        if toPos == None:
            toPos = (self.width, self.height)
        for item in self.staticEssences:
            screen.blit(item.image, item.rect)

    def renderCells(self, screen, pos=(0, 0), pos2=None, xMax=0) :
        if pos2 is None:
            pos2 = (pos[0] + 20, pos[1] + 15)
        self.surface.fill(self.BLACK)
        iX = 0
        iY = 0
        for i in range(pos[0], pos2[0] + 1):
            iY = 0
            for j in range(pos[1], pos2[1] + 1):
                if i <= self.width and j <= self.height:
                    pygame.draw.rect(self.surface, self.colors[self.cells[i][j]], (self.x + iX * self.cellSize,
                                                             self.y + iY * self.cellSize, self.cellSize, self.cellSize))
                else:
                    pygame.draw.rect(self.surface, COLORS.BLACK, (self.x + iX * self.cellSize,
                                                             self.y + iY * self.cellSize, self.cellSize, self.cellSize), 3)
                iY += 1
            iX += 1
        self.renderStaticEssenses(self.surface, fromPos=pos, toPos=(pos[0] + pos2[0], pos[1] + pos2[1]))
        screen.blit(self.surface, (int((xMax - self.cellSize * pos2[0]) / 2), 0))