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


    def render(self, screen, width):
        if self.board is None:
            print("ERROR NO SELECTED BOARD IN CAMERA")
            return None
        if self.selected is None:
            print("ERROR NO SELECTED ESSENCE IN CAMERA")
            return None
        # center poses
        self.selected = self.board.movePlayer(self.selected)
        lX ,lY = self.board.get_cell((self.selected.x + self.selected.rect.width, self.selected.y + self.selected.rect.height))
        if lX <= self.width:
            lX = self.width + 1
        if lY <= self.height:
            lY = self.height + 1
        self.board.renderCells(
            screen, xMax=width, pos=(lX-self.width - 1, lY - self.height - 1), pos2=(lX+self.width+1, lY+self.height+1))
