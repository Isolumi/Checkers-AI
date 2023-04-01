""" Checkers Piece class

Module Description
==================

This module contains a collection of functions and attributes that will be used to represent pieces on a gameboard.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""
from __future__ import annotations
from .constants import *
from python_ta.contracts import check_contracts


@check_contracts
class Piece:
    """ A class representing a piece in the game.

    Instance Attributes:
    - row: The piece's row location.
    - col: The piece's column location.
    - colour: The colour of the piece.
    - is_king: Whether this piece is a king or not.
    - x_pos: The x-coordinate of the center of the piece on the screen.
    - y_pos: The y-coordinate of the center of the piece on the screen.

    Constants:
    - PADDING : The padding distance between the piece and the border of the square.
    - OUTLINE : The radius of the outline circle of the piece.

    Representation Invariants:
    - row < ROWS and row >= 0
    - col < COLS and col >= 0
    - colour in ((255, 255, 255), (0, 0, 0))
    - x_pos is within the size of the screen
    - y_pos is within the size of the screen
    """
    row: int
    col: int
    colour: tuple[int, int, int]
    is_king: bool
    x_pos: int
    y_pos: int

    PADDING = int
    OUTLINE = int

    def __init__(self, row: int, col: int, colour: tuple[int, int, int]) -> None:
        """ Initializes a new piece object

        Parameters:
        - row: The piece's row location.
        - col: The piece's column location.
        - colour: The colour of the piece.

        Preconditions:
        - row < ROWS and row >= 0
        - col < COLS and col >= 0
        - colour in ((255, 255, 255), (0, 0, 0))
        """
        self.row = row
        self.col = col
        self.colour = colour
        self.is_king = False
        self.x_pos = 0
        self.y_pos = 0
        self.PADDING = 10
        self.OUTLINE = 45
        self.calc_position()

    def calc_position(self) -> None:
        """ Calculates the x,y-coordinates of the center of the piece on the screen """
        self.x_pos = (SQUARE_SIZE * self.col) + (SQUARE_SIZE // 2)
        self.y_pos = (SQUARE_SIZE * self.row) + (SQUARE_SIZE // 2)

    def make_king(self) -> None:
        """ Makes thet piece a king """
        self.is_king = True

    def move(self, row: int, col: int) -> None:
        """ Adjusts the piece's row, column coordinates

        Parameters:
        - row: The new row index of the piece.
        - col: the new column index of the piece.

        Preconditions:
        - row < ROWS and row >= 0
        - col < COLS and col >= 0
        """
        self.row = row
        self.col = col
        self.calc_position()

    def draw(self, screen: pygame.Surface) -> None:
        """ Draws the piece of the screen

        Parameters:
        - screen: The pygame surface object to draw the piece on.

        Preconditions:
        - screen is a valid pygame surface object.
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(screen, GREY, (self.x_pos, self.y_pos), self.OUTLINE)
        pygame.draw.circle(screen, self.colour, (self.x_pos, self.y_pos), radius)

        if self.is_king:
            screen.blit(CROWN, (self.x_pos - CROWN.get_width() // 2, self.y_pos - CROWN.get_height() // 2))


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
