""" piece """
import pygame
from .constants import *


class Piece:
    """ Piece """
    PADDING = 10
    OUTLINE = 45

    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        """ calc pos """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        """ making self a king """
        self.king = True

    def draw(self, win):
        """ draws the pieces """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), self.OUTLINE)
        pygame.draw.circle(win, self.colour, (self.x, self.y), radius)
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))


    def move(self, row, col):
        """ updates piece location """
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.colour)
