""" Game """

from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts
from Piece import Piece
from Board import Board
from Player import Player


@check_contracts
class Game:
    """
    Instance Attributes:

    Representation Invariants:
    """
    board: Board
    players: tuple[Player, Player]

    def __init__(self, board: Board, players: tuple[Player, Player]):
        self.board = board
        self.players = players
