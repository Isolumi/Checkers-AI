import pygame
from .constants import *


class Piece:
    row: int
    col: int
    colour: tuple[int, int, int]
    is_king: bool
    x_pos: int
    y_pos: int

    PADDING = 10 # TODO: maybe put this in init
    OUTLINE = 45

    def __init__(self, row: int, col: int, colour: tuple[int, int, int]) -> None:
        self.row = row
        self.col = col
        self.colour = colour
        self.is_king = False
        self.x_pos = 0
        self.y_pos = 0
        self.calc_position()

    def calc_position(self) -> None:
        self.x_pos = (SQUARE_SIZE * self.col) + (SQUARE_SIZE // 2)
        self.y_pos = (SQUARE_SIZE * self.row) + (SQUARE_SIZE // 2)

    def make_king(self) -> None:
        self.is_king = True

    def draw(self, win: pygame.Surface) -> None:
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x_pos, self.y_pos), self.OUTLINE)
        pygame.draw.circle(win, self.colour, (self.x_pos, self.y_pos), radius)

        if self.is_king:
            win.blit(CROWN, (self.x_pos - CROWN.get_width() // 2, self.y_pos - CROWN.get_height() // 2))


    def move(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.calc_position()

    def __repr__(self) -> str:
        return str(self.colour)
