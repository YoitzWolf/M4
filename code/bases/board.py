import pygame
import math
import time
import random
import copy

from bases.colors import COLORS
import bases.interfaces as INTERFACE


class BOARD():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cellSize = None
        self.BLACK = COLORS.BLACK
        self.x = 0
        self.y = 0
        self.cells = [[-1] * (self.width + 10)
                      for i in range(self.height + 10)]
        self.surface = pygame.Surface([1, 1])
    
    def setCoords(self, x, y):
        self.x = x
        self.y = y

    def resize(self, x, y):
        self.width = x
        self.height = y
        newCells = [[-1] * self.width for i in range(self.height)]
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

    def on_click(self, cell):
        print(cell)

    def click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def autoSizer(self, width, height):
        self.cellSize = int(min(width / self.width, height / self.height))
        self.surface = pygame.Surface([self.width * self.cellSize, self.height * self.cellSize])

    def renderCells(self, screen, xMax, yMax):
        self.surface.fill(self.BLACK)
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(self.surface, self.BLACK, (self.x + i * self.cellSize,
                                                         self.y + j * self.cellSize, self.cellSize, self.cellSize))
                pygame.draw.rect(self.surface, (200, 200, 200), (self.x + i * self.cellSize,
                                                           self.y + j * self.cellSize, self.cellSize, self.cellSize), 1)
        screen.blit(self.surface, (int((xMax -  self.cellSize * self.width) / 2), 0))