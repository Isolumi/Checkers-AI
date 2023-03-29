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
    A class representing a  game of Checkers. Contains a board represented using the board class,
     a tuple containing the players of the game (the player and the AI opponent), and an
    indicator as to which player's turn it is.

    Instance Attributes:
        - board: an 8x8 representation of a board using a list of lists containing positions on the board
        - players: a tuple containing the 2 instances of the player class. The first entry in the tuple
        will be the player, and the second entry is the opponent AI
        - turn: a string that says whether the current turn is of the player or the opponent, using 2 possible
        options of 'player' or 'opponent'

    Representation Invariants:
        - self.players[1].is_ai is True
        - self.turn in {'player', 'opponent'}
    """
    board: Board
    players: tuple[Player, Player]
    turn: str

    def __init__(self, board: Board, players: tuple[Player, Player]):

        self.board = board
        self.players = players
        self.turn = 'player'

    def get_winner(self) -> Optional[str]:  # Will be called every time a turn is made to check conditions
        """Check whether the player or opponent have won the game based on 2 factors:
            - If a player cannot make a move with any piece, the other player] wins
            - If a player does not have any remaining pieces, the other player wins
        """
        if self.turn == 'player':
            enemy = self.players[1]

            if len(enemy.materials) == 0:  # Checking whether enemy has pieces
                return "Congratulations, you win!"
            lst = []
            for piece in enemy.materials:
                lst.append(piece.possible_moves == set())
            if all(lst):  # Checking if enemy is able to make any moves
                return "Congratulations, you win!"
            else:
                return None
        else:
            player = self.players[0]
            if len(player.materials) == 0:  # Checking whether player has pieces
                return "Sorry, you lose. You'll get \'em next time!"
            lst = []
            for piece in player.materials:
                lst.append(piece.possible_moves == set())
            if all(lst):  # Checking if player is able to make any moves
                return "Sorry, you lose. You'll get \'em next time!"
            else:
                return None
