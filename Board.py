""" Board """

from __future__ import annotations
from python_ta.contracts import check_contracts
from Piece import Piece


@check_contracts
class Board:
    """
    Instance Attributes:
        - board: a 8x8 matrix that will represent the game board

    Representation Invariants:
        - board is 8x8
    """
    board: tuple[list[Piece]]

    def __init__(self, board: tuple[list[Piece]]):
        self.board = board
