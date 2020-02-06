import pygame

import bases.interfaces as INTERFACE


class CAMERA(INTERFACE.CONTROLLED):
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.deltaX = 0
        self.deltaY = 0
        self.board = None
        self.width = width
        self.height = height
        self.selected = None
        self.keys = {}
        self.initControlKeys({
                    "forward": [274, 115],
                    "back": [273, 119],
                    "right": [275, 100],
                    "left": [276, 97]
                })

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
        self.board.autoSizer(width, height, self.width, 5)
        self.selected = self.board.resizeEssences()

    def keysInterpretator(self, key, activated):
        self.keys[key] = activated
        if self.selected is not None and self.selected.useable(key):
            self.selected.keyManager(key, activated)
        '''
        if activated:
            if key in self.forward:
                self.y += 1
            if key in self.back:
                self.y -= 1
            if key in self.right:
                self.x += 1
            if key in self.left:
                self.x -= 1
        '''


    def selectedModelPosManager(self):
        last = self.selected.x, self.selected.y
        self.selected = self.board.movePlayer(self.selected, self.width, self.height)
        new = self.selected.x, self.selected.y
        self.deltaX += new[0] - last[0]
        self.deltaY += new[1] - last[1]

    def render(self, screen, width):
        if self.board is None:
            print("ERROR NO SELECTED BOARD IN CAMERA")
            return None
        if self.selected is None:
            print("ERROR NO SELECTED ESSENCE IN CAMERA")
            return None
        #player = self.board.get_cell(self.selected.x, self.selected.y)
        # center poses
        self.board.renderCells(screen,delta=(self.deltaX, self.deltaY))
