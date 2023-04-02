""" Checkers gametree class

Module Description
==================

This module contains a collection of functions and attributes that will be used to represent the gametree in which
the AI will select moves from.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""

from __future__ import annotations
from python_ta.contracts import check_contracts
from .board import Board
from .constants import *


# @check_contracts
class GameTree:
    """
    Instance Attributes:
        - move: the previous move made in the checkers game.
        - material_advantage: the current advantage of white at the current state of the gameboard.
        - board_state: a board instance showing the state of the current board.

    Private Instance Attributes:
        - _subtrees: maps a board to a GameTree.

    Representation Invariants:
    - move == '*' if the game has just begun.
    """
    move: str | tuple[tuple[int, int], tuple[int, int]]
    material_advantage: float
    board_state: Board

    _subtrees: dict[str, GameTree]

    def __init__(self,  board: Board, move: str | tuple[tuple[int, int], tuple[int, int]] = '*',
                 material_adv: float = 0.0) -> None:
        """ Initializing new GameTree """
        self.move = move
        self.material_advantage = material_adv
        self._subtrees = {}
        self.board_state = board

    def get_subtrees(self) -> list[GameTree]:
        """ Returns the subrees in this GameTree """
        return list(self._subtrees.values())

    def __len__(self) -> int:
        """ Returns the number of items in this tree """
        return 1 + sum(len(subtree) for subtree in self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """ Add a subtree to this game tree.

        Parameters:
        - subtree: the subtree to be added to self
         """
        self._subtrees[str(subtree.board_state)] = subtree


def generate_game_tree(board: Board, m: tuple[tuple[int, int], tuple[int, int]], d: int = 0) -> GameTree:
    """ generates the gametree up to a certain depth with all the possible moves

    Parameters:
    - board: the current state of the baord in which to build the gametree upon.
    - m: the move that was made to achieve the current state of the board.
    - d: recurrsion variable to keep track of depth.

    Returns:
    - returns a GameTree object that contatins all the valid moves for a given board.
     """
    game_tree = GameTree(board)
    game_tree.move = m

    if d == 4:
        black_adv = board.black_left + (2 * board.black_kings)
        white_adv = board.white_left + (2 * board.white_kings)
        game_tree.material_advantage = black_adv - white_adv
        return game_tree
    else:
        for row in board.board:
            for piece in row:
                if piece == 0:
                    pass
                elif piece.colour == BLACK and d % 2 == 0:
                    for cord in list(board.get_valid_moves(piece).keys()):
                        board_copy = board.__copy__()
                        move = ((piece.row, piece.col), cord)
                        board_copy.move(board_copy.board[piece.row][piece.col], cord[0], cord[1])
                        remove_pieces = board.get_valid_moves(piece)[cord]
                        board_copy.remove(remove_pieces)
                        new_game_tree = generate_game_tree(board_copy, move, d + 1)

                        if len(new_game_tree.get_subtrees()) == 0:
                            b_adv = new_game_tree.board_state.black_left + 2 * new_game_tree.board_state.black_kings
                            w_adv = new_game_tree.board_state.white_left + 2 * new_game_tree.board_state.white_kings
                            new_game_tree.material_advantage = b_adv - w_adv
                        else:
                            tot = sum([tree.material_advantage for tree in new_game_tree.get_subtrees()])
                            new_game_tree.material_advantage = tot / len(new_game_tree.get_subtrees())

                        game_tree.add_subtree(new_game_tree)
                elif piece.colour == WHITE and d % 2 != 0:
                    for cord in list(board.get_valid_moves(piece).keys()):
                        board_copy = board.__copy__()
                        move = ((piece.row, piece.col), cord)
                        board_copy.move(board_copy.board[piece.row][piece.col], cord[0], cord[1])
                        remove_pieces = board.get_valid_moves(piece)[cord]
                        board_copy.remove(remove_pieces)
                        new_game_tree = generate_game_tree(board_copy, move, d + 1)

                        if len(new_game_tree.get_subtrees()) == 0:
                            b_adv = new_game_tree.board_state.black_left + 2 * new_game_tree.board_state.black_kings
                            w_adv = new_game_tree.board_state.white_left + 2 * new_game_tree.board_state.white_kings
                            new_game_tree.material_advantage = b_adv - w_adv
                        else:
                            tot = sum([tree.material_advantage for tree in new_game_tree.get_subtrees()])
                            new_game_tree.material_advantage = tot / len(new_game_tree.get_subtrees())

                        game_tree.add_subtree(new_game_tree)

        if len(game_tree.get_subtrees()) != 0:
            tot = sum([tree.material_advantage for tree in game_tree.get_subtrees()])
            game_tree.material_advantage = tot / len(game_tree.get_subtrees())

        return game_tree


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120
    })
