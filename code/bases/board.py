import pygame
import math
import time
import random
import copy


class BOARD():

    def __init__(self, width, height, cellSize=30, x=0, y=0):
        self.width = width
        self.height = height
        self.cellSize = cellSize
        self.x = x
        self.y = y
        self.cells = [[-1] * (self.width + 10)
                      for i in range(self.height + 10)]
        self.color = [(1, 1, 1), (0, 0, 255), (255, 0, 0)]

    def setView(self, x, y, size):
        self.x = x
        self.y = y
        self.cellSize = size

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
        pass

    def click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)

    def renderCells(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, self.color[0], (self.x + i * self.cellSize,
                                                         self.y + j * self.cellSize, self.cellSize, self.cellSize))
                pygame.draw.rect(screen, self.color[1], (self.x + i * self.cellSize,
                                                         self.y + j * self.cellSize, self.cellSize, self.cellSize))
                pygame.draw.rect(screen, (200, 200, 200), (self.x + i * self.cellSize,
                                                           self.y + j * self.cellSize, self.cellSize, self.cellSize), 1)