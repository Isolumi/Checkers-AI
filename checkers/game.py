import pygame
from typing import Optional
from .constants import *
from .board import Board
from .piece import Piece


class Game:
    screen: pygame.Surface
    selected: Optional[Piece]
    board: Board
    turn: tuple[int, int, int]
    valid_moves: dict  # TODO: fix this

    def __init__(self, screen: pygame.Surface) -> None:
        self._init()
        self.screen = screen

    def _init(self) -> None:
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def update(self) -> None:
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self) -> Optional[tuple[tuple[int, int, int], list[list[Piece | int]]]]:
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
        elif piece == 0 or piece.colour != self.turn:
            self.selected = None
            self.valid_moves = {}

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

    def draw_valid_moves(self, moves):  # TODO do the parameter stuff
        for move in moves:
            row, col = move
            pygame.draw.rect(self.screen, LIGHT_RED,
                             (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def change_turn(self) -> None:
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_board(self) -> Board:
        return self.board
