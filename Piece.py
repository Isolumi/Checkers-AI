""" Piece """

from __future__ import annotations
from python_ta.contracts import check_contracts


@check_contracts
class Piece:
    """
    Instance Attributes:
        - possible_moves: set of legal moves that could be made by self
        - is_king: determines whether self is a king piece or not

    Representation Invariants:
    """
    possible_moves: set #TODO make sure to specific type of thing in the set
    is_king: bool

    def __init__(self, possible_moves: set, is_king: bool = False):
        self.possible_moves = possible_moves
        self.is_king = is_king
