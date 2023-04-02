""" Checkers Board class

Module Description
==================

This module contains a collection of functions and attributes that will be used to represent a checkers board.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""
from __future__ import annotations
from typing import Optional
from .constants import *
from .piece import Piece
from copy import deepcopy
from python_ta.contracts import check_contracts
import pygame


# @check_contracts
class Board:
    """ A class representing a board in the game of checkers.

    Instance Attributes:
    - board: a matrix of pieces objects or 0 if a piece does not exist.
    - white_left : integer representing number of white pieces left
    - black_left : integer representing number of black pieces left
    - white_kings : integer representing number of white king pieces
    - black_kings : integer representing number of black king pieces

    Representation Invariants:
    - self.white_left >= 0
    - self.black_left >= 0
    - self.white_kings >= 0 and self.white_kings <= 12
    - self.black_kings >= 0 and self.black_kings <= 12
    """
    board: list[list[Piece | int]]
    white_left: int
    black_left: int
    white_kings: int
    black_kings: int

    def __init__(self) -> None:
        """ Initializes an instance of a new gameboard """
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self._create_board()

    def __copy__(self) -> Board:
        """ Creates and returns a copy of the board """
        new_board = Board()
        new_board.white_left = self.white_left
        new_board.black_left = self.black_left
        new_board.white_kings = self.white_kings
        new_board.black_kings = self.black_kings

        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                if isinstance(self.board[i][j], Piece):
                    new_board.board[i][j] = self.board[i][j].__copy__()
                else:
                    new_board.board[i][j] = self.board[i][j]

        return new_board

    def _create_board(self) -> None:
        """ Creates the initial state of a gameboard """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, screen: pygame.Surface) -> None:
        """ Draws the gameboard AND the pieces on the board

        Parameters:
        - screen: a pygame surface object which will be used to display the gameboard

        Preconditions:
        - screen is an appropriate pygame surface object
        """
        self.draw_squares(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)

    def draw_squares(self, screen: pygame.Surface) -> None:
        """ Draws the squares on the gameboard WITHOUT any pieces

        Parameters:
        - screen: a pygame surface object which will be used to display the gameboard

        Preconditions:
        - screen is an appropriate pygame surface object
        """
        screen.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(screen, LIGHT_BROWN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece: Piece, row: int, col: int) -> None:
        """ Moves a piece of the board to a given row and column.

        Parameters:
        - piece: the targeted piece to be moved.
        - row: the row of the piece's destination.
        - col: the column of the piece's destination.

        Preconditions:
        - any([piece in r for r in self.board])
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.colour == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row: int, col: int) -> Piece | int:
        """ Returns the piece at the given row and column

        Parameters:
        - row: the row to get the piece from.
        - col: the column to get the piece from.

        Preconditions:
        - row < ROWS and row >= 0
        - col < COLS and col >= 0
        """
        return self.board[row][col]

    def remove(self, pieces: list[Piece]) -> None:
        """ Removes a given list of pieces from the game board.

        Parameters:
        - pieces: a list of pieces to be removes.

        Preconditions:
        - all the pieces are in self.board.
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self) -> Optional[tuple[tuple[int, int, int], list[list[Piece | int]]]]:
        """ Determines and returns the winner of the game if any """
        if self.white_left <= 0:
            return (BLACK, self.board)
        elif self.black_left <= 0:
            return (WHITE, self.board)
        else:
            return None

    def get_valid_moves(self, piece: Piece) -> dict[tuple[int, int], list[Piece]]:
        """ Returns a dictionary of valid moves for a given piece.

        Parameters:
        - piece: the piece for whicih valid mores are to be determines.

        Returns:
        - A dictionary where the keys reprsents the coordinates of valid moves for the piece and
        the values represent the pieces that would be captured if a piece were to move to the location
        of the key.

        Preconditions:
        - piece is a valid piece object in self.board.
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.colour == WHITE or piece.is_king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.colour, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.colour, right))

        if piece.colour == BLACK or piece.is_king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.colour, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.colour, right))

        return moves

    def _traverse_left(self, start: int, stop: int, direction: int, colour: tuple[int, int, int], col,
                       captured: list = None) -> dict[tuple[int, int], list[Piece]]:
        """ Helper function for self.get_valid_moves. Traverses diagonally left and returns a dictionary
        of valid moves and captured pieces if any

        Parameters:
        - start: the row index to begin traversing from.
        - stop: the row index to stop traversing.
        - direction: direction of traverse (up or down).
        - colour: the colour of the traversing piece.
        - col: the column of traversing.
        - captured: a list of captured pieces during the traversal.

        Returns:
        - A dictionary where the keys reprsents the coordinates of valid moves for the piece and
        the values represent the pieces that would be captured if a piece were to move to the location
        of the key.

        Preconditions:
        - start <= ROWS and start >= -1
        - stop <= ROWS and stop >= -1
        - direction in (-1, 1)
        - colour in ((255, 255, 255), (0, 0, 0))
        - col <= COLS and col >= -1
        - captured is a valid list of pieces or None
        """
        if captured is None:
            captured = []
        moves = {}
        last = []

        for r in range(start, stop, direction):
            if col < 0:
                break

            current = self.board[r][col]
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, col)] = last + captured
                else:
                    moves[(r, col)] = last

                if last:
                    if direction == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + direction, row, direction, colour, col - 1, captured=last))
                    moves.update(self._traverse_right(r + direction, row, direction, colour, col + 1, captured=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]
            col -= 1

        return moves

    def _traverse_right(self, start: int, stop: int, direction: int, colour: tuple[int, int, int], col,
                        captured: list = None) -> dict[tuple[int, int], list[Piece]]:
        """ Helper function for self.get_valid_moves. Traverses diagonally left and returns a dictionary
        of valid moves and captured pieces if any

        Parameters:
        - start: the row index to begin traversing from.
        - stop: the row index to stop traversing.
        - direction: direction of traverse (up or down).
        - colour: the colour of the traversing piece.
        - col: the column of traversing.
        - captured: a list of captured pieces during the traversal.

        Returns:
        - A dictionary where the keys reprsents the coordinates of valid moves for the piece and
        the values represent the pieces that would be captured if a piece were to move to the location
        of the key.

        Preconditions:
        - start <= ROWS and start >= -1
        - stop <= ROWS and stop >= -1
        - direction in (-1, 1)
        - colour in ((255, 255, 255), (0, 0, 0))
        - col <= COLS and col >= -1
        - captured is a valid list of pieces or None
        """
        if captured is None:
            captured = []
        moves = {}
        last = []

        for r in range(start, stop, direction):
            if col >= COLS:
                break

            current = self.board[r][col]
            if current == 0:
                if captured and not last:
                    break
                elif captured:
                    moves[(r, col)] = last + captured
                else:
                    moves[(r, col)] = last

                if last:
                    if direction == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)

                    moves.update(self._traverse_left(r + direction, row, direction, colour, col - 1, captured=last))
                    moves.update(self._traverse_right(r + direction, row, direction, colour, col + 1, captured=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]
            col += 1

        return moves


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
