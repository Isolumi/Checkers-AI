""" GameTree """

from __future__ import annotations
from typing import List, Optional
from python_ta.contracts import check_contracts
from Board import Board
from project.CheckersAI.Board import Board


@check_contracts
class GameTree:
    """
    Instance Attributes:
        - move
        - player_win_probability

    Private Instance Attributes:
        - _board_state:
        - _subtrees:

    Representation Invariants:
    """
    move: str
    white_win_probability: float

    _board_state: Board
    _subtrees: dict[tuple[tuple[int]], GameTree]

    def __init__(self, move: str, white_win_probability: float = 0.0) -> None:
        """ Initializing new GameTree """
        self.move = move
        self.white_win_probability = white_win_probability
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """ Returns the subrees in this GameTree"""
        return list(self._subtrees.values())

    def find_subtree(self, move: tuple[tuple[int]]) -> Optional[GameTree]:
        """ Returns the subtree corresponding to the given move. """
        if move in self._subtrees:
            return self._subtrees[move]

    def __len__(self) -> int:
        """ Returns the number of items in this tree """
        return 1 + sum(len(subtree) for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """ Add a subtree to this game tree. """
        self._subtrees[#TODO: board to str???] = subtree
