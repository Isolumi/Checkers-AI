""" Constants

Module Description
==================

This module contains a collection of constants that will be used throughout the implementation of the checkers game.

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""
import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# RGB values
RED = (255, 0, 0)
LIGHT_RED = (200, 75, 75)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
DARK_GREY = (105, 105, 105)
BLUE = (0, 0, 255)
DARK_BROWN = (116, 52, 16)
DARK_BROWN2 = (74, 55, 43)
LIGHT_BROWN = (236, 205, 165)
LIGHT_BROWN2 = (213, 202, 191)


CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (50, 45))
