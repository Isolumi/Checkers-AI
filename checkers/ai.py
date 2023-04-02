from __future__ import annotations
from .gametree import *
from python_ta.contracts import check_contracts
from .board import Board
from .constants import *


# @check_contracts
class AI:
    """ A player class that makes moves based on the game tree
    """
    game_tree: GameTree

    def __init__(self, game_tree: GameTree) -> None:
        self.game_tree = game_tree

    def update_game_tree(self, move: tuple[tuple[int, int], tuple[int, int]], board: Board) -> None:
        self.game_tree = generate_game_tree(board, move)

    def make_move(self) -> tuple[tuple[int, int], tuple[int, int]] | str:
        moves = self.game_tree.get_subtrees()
        curr_advantage = -100
        best = moves[0]

        for move in moves:
            if move.material_advantage > curr_advantage:
                curr_advantage = move.material_advantage
                best = move

        self.game_tree = best
        return best.move
