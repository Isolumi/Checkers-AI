""" GameTree """

from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts
from .board import Board
from .constants import *


@check_contracts
class GameTree:
    """
    Instance Attributes:
        - move
        - player_win_probability

    Private Instance Attributes:
        - _board_state: a board instance showing the state of the current board.
        - _subtrees: maps a board_state to a GameTree.

    Representation Invariants:
    """
    move: str | tuple[tuple[int, int], tuple[int, int]]
    material_advantage: float

    _board_state: Board
    _subtrees: dict[str, GameTree]

    def __init__(self,  board: Board, move: str | tuple[tuple[int, int], tuple[int, int]] = '*', material_adv: float = 0.0) -> None:
        """ Initializing new GameTree """
        self.move = move
        self.material_advantage = material_adv
        self._subtrees = {}
        self._board_state = board

    def get_subtrees(self) -> list[GameTree]:
        """ Returns the subrees in this GameTree"""
        return list(self._subtrees.values())

    def find_subtree(self, board_state: str) -> Optional[GameTree]:
        """ Returns the subtree corresponding to the given _board_state. """
        if board_state in self._subtrees:
            return self._subtrees[board_state]

    def __len__(self) -> int:
        """ Returns the number of items in this tree """
        return 1 + sum(len(subtree) for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """ Add a subtree to this game tree. """
        self._subtrees[str(subtree._board_state)] = subtree

    def insert_move_sequence(self, board_statuses: list[Board], curr_index: int = 0) -> None:
        """ Insert a sequence of board statuses """
        if curr_index == len(board_statuses):
            return

        if self.find_subtree(str(board_statuses[curr_index])) is not None:
            self.find_subtree(str(board_statuses[curr_index])).insert_move_sequence(board_statuses, curr_index + 1)
        else:
            new_board = GameTree(str(board_statuses[curr_index]))
            new_board.insert_move_sequence(board_statuses, curr_index + 1)


def generate_game_tree(board: Board, d: int = 0) -> GameTree:
    game_tree = GameTree(board=Board)

    if d == 5:
        return GameTree(board=Board, material_diff=board.black_left - board.white_left)
    else:
        for row in board.board:
            for piece in row:
                if piece.colour == BLACK:
                    for cord in board.get_valid_moves(piece).keys():
                        board_copy = board.__copy__()
                        board_copy.move(piece, cord[0], cord[1])
                        move = ((piece.row, piece.col), cord) #I'm assuming cord is a tuple of (r,c)
                        new_game_tree = generate_game_tree(board_copy, d + 1)
                        new_game_tree.material_advantage = sum([tree.material_advantage for tree in new_game_tree.get_subtrees()]) / len(new_game_tree.get_subtrees())
                        new_game_tree.move = move
                        game_tree.add_subtree(new_game_tree)

        return game_tree


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
