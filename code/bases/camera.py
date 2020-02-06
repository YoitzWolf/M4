import pygame

class CAMERA():
    def __init__(self, width, height):
        self.board = None
        self.width = width
        self.height = height
        self.selected = None
        self.keys = {}

    def setSize(self, width, height):
        self.width = width
        self.height = height

    def setCameraSelection(self, essence):
        if self.board is not None:
            self.selected = essence
            self.selected = self.board.insertPlayer(self.selected)
        else:
            print("ERROR NO SELECTED BOARD IN CAMERA")

    def setCameraBoard(self, board):
        self.board = board

    def boardSizer(self, width, height):
        self.board.autoSizer(width, height, self.width * 2 + 1, self.height * 2 + 1)
        self.board.resizeEssences()

    def keysInterpretator(self, key, activated):
        self.keys[key] = activated
        if self.selected is not None and self.selected.useable(key):
            self.selected.keyManager(key, activated)

    def selectedModelPosManager(self):
        self.selected = self.board.movePlayer(self.selected, self.width, self.height)

    def render(self, screen, width):
        if self.board is None:
            print("ERROR NO SELECTED BOARD IN CAMERA")
            return None
        if self.selected is None:
            print("ERROR NO SELECTED ESSENCE IN CAMERA")
            return None
        # center poses
        self.board.renderCells(
            screen, size=(self.width, self.height), centered=self.selected, xMax=width)
