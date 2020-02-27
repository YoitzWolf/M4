import pygame
from classes.screens import STRATER

if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((600, 320), pygame.RESIZABLE)
    game = STRATER(screen, pygame.quit, pygame.display.flip)
    game.loop()
