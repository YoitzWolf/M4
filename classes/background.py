import pygame
import math
import time
import random
import copy

from classes.colors import COLORS
from classes.datatypes import SPRITE_DEQUE
from classes.essences import BACK_SPRITE_UNIT
from classes.essences import BACKGROUND_IMAGE
import classes.interfaces as INTERFACES


class BACKGROUND():
	def __init__(self, w, h, cells_in_line=16, rules={}):

		self.info = rules

		self.fontNormal = pygame.font.Font(self.info['FONTS']['FONT'], ( min(w, h) // cells_in_line))

		self.colors = COLORS()
		self.pos = 0
		self.cells_in_line = cells_in_line
		self.lines_count = int(cells_in_line * 1.5)

		self.cellSize = min(int(h // self.cells_in_line), int(w // self.lines_count))

		self.h = self.cellSize * self.cells_in_line
		self.w = self.cellSize * self.lines_count

		self.surface = pygame.Surface((self.w + self.cellSize, self.h), pygame.SRCALPHA, 32)
		self.lines = SPRITE_DEQUE()
		self.speed = 1 # cells per second
		'''
		self.image = BACKGROUND_IMAGE("data/bg", "/back.png")
		self.image.load()
		self.image.setSize(self.w, self.h)
		'''

	def move(self, tick):
		#tick in milliseconds
		#delta = (tick/1000) * (self.speed * self.cellSize)
		#self.pos += delta
		#while int(self.pos) > 0:
		#	self.add_line()
		#	self.pos -= self.cellSize
		#while self.pos + self.cellSize * (self.lines.size() - 1) > self.h:
		#	self.lines.pop_back()
		pass

	def newSprite(self):
		name=("data/bg", "/bg_var_1.png")
		sprite = BACK_SPRITE_UNIT(self.cellSize, name=name, rand=100)
		return sprite

	def add_row(self):
		line = [self.newSprite()] * self.cells_in_line

		self.lines.push_front(line)

	def render(self, screen, w, h):
		self.surface = pygame.Surface((self.w, self.h + self.cellSize), pygame.SRCALPHA, 32)

		for i in range(self.lines.size()):
			for j in range(len(self.lines.get_by_i(i))):
				self.lines.get_by_i(i)[j].render(self.surface, i * self.cellSize, j * self.cellSize)


		# screen.blit(self.surface, ((w - self.w)//2, self.pos + (h - self.h)//2))

	def resize(self, w, h):
		self.cellSize = min(int(h // self.cells_in_line), int(w // self.lines_count))

		self.h = self.cellSize * self.cells_in_line
		self.w = self.cellSize * self.lines_count

		self.surface = pygame.Surface((self.w + self.cellSize, self.h), pygame.SRCALPHA, 32)

		self.lines.resizeAll(self.cellSize)
