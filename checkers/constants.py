import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# -- RGB --

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
DARK_BROWN = (116, 52, 16)
LIGHT_BROWN = (236, 205, 165)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (50, 45))
