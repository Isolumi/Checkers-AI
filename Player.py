""" Represents a Player in a Checkers game """

from __future__ import annotations
from typing import Optional
from python_ta.contracts import check_contracts
from Piece import Piece


@check_contracts
class Player:
    """
    Instance Attributes:
        - is_ai: whether this player is an AI or not
        - colour: the colour of this player's pieces
        - materials: represents a player's pieces and its respective location on the game board
        - points: the amount of points a player currently has

    Representation Invariants:
        - points >= 0
    """
    is_ai: bool
    colour: str
    materials: dict[str, Piece]
    points: int

    def __init__(self, is_ai: bool, colour: str, material: dict[str, Piece], points: Optional[int]):
        self.is_ai = is_ai
        self.colour = colour
        self.materials = material
        self.points = points
