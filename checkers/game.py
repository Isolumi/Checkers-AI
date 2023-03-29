from typing import Optional

import pygame
from .constants import *
from .board import Board
from .piece import Piece


class Game:
    win: pygame.Surface
    selected: Optional[Piece]
    board: Board
    turn: tuple[int, int, int]
    valid_moves: dict #TODO: fix this

    def __init__(self, win: pygame.Surface) -> None:
        self._init()
        self.win = win

    def _init(self) -> None:
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def update(self) -> None:
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self) -> tuple[int, int, int]:
        return self.board.winner()

    def reset(self) -> None:
        self._init()

    def select(self, row: int, col: int) -> bool:
        if self.selected is not None:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.colour == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row: int, col: int) -> bool:
        piece = self.board.get_piece(row, col)

        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self.board.remove(captured)

            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves): #TODO do the parameter stuff
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self) -> None:
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_board(self) -> Board:
        return self.board
