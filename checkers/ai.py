from __future__ import annotations
from .gametree import GameTree
from python_ta.contracts import check_contracts
from .board import Board
from .constants import *


@check_contracts
class AI:
    """ A player class that makes moves based on the game tree
    """
    game_tree: GameTree

    def __init__(self, game_tree: GameTree) -> None:
        self.game_tree = game_tree

    def update_game_tree(self) -> None:
        raise NotImplementedError

    def make_move(self) -> tuple[int, int]:
        moves = self.game_tree.get_subtrees()
        curr_advantage = 0
        best = ...

        for move in moves:
            if move.material_advantage > curr_advantage:
                curr_advantage = move.material_advantage
                best = move

        self.game_tree = best
        return best._board_state
