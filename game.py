""" Checkers Game class

Module Description
==================

This module contains a collection of functions and attributes that will be used to help run the whole checkers game.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""
from __future__ import annotations
from typing import Optional
import pygame
from constants import *
from board import Board
from piece import Piece


# from python_ta.contracts import check_contracts


# @check_contracts
class Game:
    """ Represents a game of checkers

    Instance Attribute:
    - screen: the pygame screen object on which the game is displayed.
    - selected: the piece that the player has selected with their mouse.
    - turn: the player whose turn it is.
    - valid_moves: a dict containing the valid moves and pieces that will be captured.
    - prev_move: the previous move made on the game board.

    Private Instance Attributes:
    - board: an instance of board used to represent the board used for the game.
    """
    screen: pygame.Surface
    selected: Optional[Piece]
    _board: Board
    turn: tuple[int, int, int]
    valid_moves: dict[tuple[int, int], list[Piece]]
    prev_move: tuple[tuple[int, int], tuple[int, int]] | str

    def __init__(self, screen: pygame.Surface) -> None:
        """ Initializes a checkers game """
        self.screen = screen
        self.selected = None
        self._board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.prev_move = '*'

    def get_board(self) -> Board:
        """ Returns a copy of the game board """
        return self._board.__copy__()

    def update(self) -> None:
        """ Updates the display of the game board """
        self._board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def select(self, row: int, col: int) -> bool:
        """ Selects a piece at the given row and column

        Parameters:
        - row: the row of the piece to select.
        - column: the column of the piece to select.

        Returns:
        - returns True if a piece has been successfully selected, and False otherwise.

        Preconditions:
        - row < ROWS and row >= 0
        - col < COLS and col >= 0
        """
        if self.selected is not None:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self._board.get_piece(row, col)
        if piece != 0 and piece.colour == self.turn:
            self.selected = piece
            self.valid_moves = self._board.get_valid_moves(piece)
            return True
        elif piece == 0 or piece.colour != self.turn:
            self.selected = None
            self.valid_moves = {}
            return False

        else:
            return False

    def _move(self, row: int, col: int) -> bool:
        """ Moves the selected piece to the given row and column

        Parameters:
        - row: the row to move the selected piece to.
        - col: the column to move the selected piece to.

        Returns:
        - True if the piece was successfully moved, False otherwise.

        Preconditions:
        - row < ROWS and row >= 0
        - col < COLS and col >= 0
        """
        piece = self._board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.prev_move = ((self.selected.row, self.selected.col), (row, col))
            self._board.move(self.selected, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self._board.remove(captured)

            self.change_turn()
            return True
        else:
            return False

    def draw_valid_moves(self, moves: dict[tuple[int, int], list[Piece]]) -> None:
        """ Highlights the valid moves on the game board.

        Parameters:
        - moves: a dictionary containing the valid moves.

        Preconditions:
        - moves is a valid dictionary of valid moves.
        """
        for move in moves:
            row, col = move
            pygame.draw.rect(self.screen, LIGHT_RED,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def change_turn(self) -> None:
        """ Changes the turn to the other player colour """
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_winner(self) -> Optional[tuple[tuple[int, int, int], list[list[Piece | int]]]]:
        """ Returns the winner of the game if there is one, otherwise returns None """
        return self._board.get_winner()


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['board', 'piece', 'pygame', 'constants'],
        'max-line-length': 120,
        'disable': ['wildcard-import']
    })
