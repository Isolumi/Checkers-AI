""" Checkers AI class

Module Description
==================

This module contains a collection of functions and attributes that will be used to represent an AI player that will
play against a human player at the game of checkers.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""
from __future__ import annotations
from .gametree import *
from python_ta.contracts import check_contracts
from .board import Board


# @check_contracts
class AI:
    """ A player class that makes moves based on the game tree

    Instance Attributes:
    - game_tree: a gametree object that the AI will use to pick the best moves.
    """
    game_tree: GameTree

    def __init__(self, game_tree: GameTree) -> None:
        """ Initializes the AI's gametree """
        self.game_tree = game_tree

    def update_game_tree(self, move: tuple[tuple[int, int], tuple[int, int]], board: Board) -> None:
        """ updates the AI's gametree after a move was made.

        Parameters:
        - move: the previous move that was made.
        - board: a board object for the current state of the gameboard.

        Preconditions:
        - move is a valid checkers move.
        - the board status matches the move that was given.
        """
        self.game_tree = generate_game_tree(board, move)

    def make_move(self) -> tuple[tuple[int, int], tuple[int, int]] | str:
        """ makes the best move for the AI player

        Returns:
        - returns the move that was made.
        """
        moves = self.game_tree.get_subtrees()
        curr_advantage = -100
        best = moves[0]

        for move in moves:
            if move.material_advantage > curr_advantage:
                curr_advantage = move.material_advantage
                best = move

        self.game_tree = best
        return best.move


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })
