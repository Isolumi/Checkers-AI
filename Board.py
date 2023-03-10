""" Board """

from __future__ import annotations

from types import NoneType

from python_ta.contracts import check_contracts
from Piece import Piece
from typing import Any, Optional


@check_contracts
class Board:
    """
    Instance Attributes:
        - board: a 8x8 matrix that will represent the game board

    Representation Invariants:
        - board is 8x8
    """
    board: list[list[Any]]

    def __init__(self, board: Optional[list[list[Any]]]):
        if board is not None:
            self.board = board
        else:
            a = Piece()
            self.board = [[5], [5]]
