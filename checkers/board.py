from typing import Optional

import pygame
from .constants import *
from .piece import Piece


class Board:
    board: list[list[Piece | int]]
    white_left: int
    black_left: int
    white_kings: int
    black_kings: int

    def __init__(self) -> None:
        self.board = []
        self.black_left = self.white_left = 12
        self.black_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win: pygame.Surface) -> None:
        win.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece: Piece, row: int, col: int) -> None:
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.colour == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1

    def get_piece(self, row: int, col: int) -> Piece:
        return self.board[row][col]

    def create_board(self) -> None:
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

    def draw(self, win: pygame.Surface) -> None:
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces: list[Piece]) -> None:
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.colour == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self) -> Optional[tuple[int, int, int]]:
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE
        else:
            return None

    def get_valid_moves(self, piece: Piece) -> dict: #TODO fix return type
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

    def _traverse_left(self, start: int, stop: int, step: int, colour: tuple[int, int, int], left, skipped: list = None) -> dict: #TODO: fix return types and parameter typings
        if skipped is None:
            skipped = []
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                    if last:
                        if step == -1:
                            row = max(r - 3, 0)
                        else:
                            row = min(r + 3, ROWS)

                        moves.update(self._traverse_left(r+step, row, step, colour, left - 1, skipped=last))
                        moves.update(self._traverse_right(r+step, row, step, colour, left + 1, skipped=last))
                    break

            elif current.colour == colour:
                break
            else:
                last = [current]
            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, colour, right, skipped: list = None) -> dict:
        if skipped is None:
            skipped = []

        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                    if last:
                        if step == -1:
                            row = max(r - 3, 0)
                        else:
                            row = min(r + 3, ROWS)

                        moves.update(self._traverse_left(r + step, row, step, colour, right - 1, skipped=last))
                        moves.update(self._traverse_right(r + step, row, step, colour, right + 1, skipped=last))
                    break

            elif current.colour == colour:
                break
            else:
                last = [current]
            right += 1

        return moves
