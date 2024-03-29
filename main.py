""" Checkers Game class

Module Description
==================

This module contains a collection of functions and attributes that will be used to help run the whole checkers game.

**NOTE**
The performance of this program may be affected by the computational power of your computer. If you are experiencing
slow run times, please head to gametree.py line-80 and lower the value d. (The higher the value of d, the better the AI)

Copyright and Usage Information
===============================

This file is Copyright (c) 2023 Hubert Xu, Ibrahim Mohammad Malik, Ryan Zhang, Vishnu Neelanath
"""

from __future__ import annotations
import pygame
import constants
from game import Game
from piece import Piece
from ai import AI
from gametree import GameTree


# @check_contracts
def main() -> None:
    """ main function where the game is run """
    FPS = 24
    SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption('Checkers!')
    pygame.init()

    run = True
    clock = pygame.time.Clock()
    game = Game(SCREEN)
    board = game.get_board()
    game_tree = GameTree(board)
    ai = AI(game_tree)
    winner = ()

    def player_turn(events: any) -> bool:
        """
        Helper function - to be run when it is the player's turn

        Parameters:
        - events : the pygame event queue
        Returns:
        - should_run : whether the game should keep running
        """
        should_run = True
        for ev in events:
            if ev.type == pygame.QUIT:
                should_run = False

            if ev.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                row_num, col_num = get_row_col_from_mouse(position)
                game.select(row_num, col_num)

        return should_run

    while run:
        clock.tick(FPS)

        if game.get_winner() is not None:
            winner = game.get_winner()
            run = False

        elif game.turn == constants.BLACK:
            board = game.get_board()
            ai.update_game_tree(game.prev_move, board)
            move = ai.make_move()
            pygame.time.delay(100)
            game.select(move[0][0], move[0][1])
            game.select(move[1][0], move[1][1])

        else:
            run = player_turn(pygame.event.get())

        game.update()

    game_over(SCREEN, winner[0], winner[1])


def get_row_col_from_mouse(pos: tuple[int, int]) -> tuple:
    """ returns the square that the user's mouse is positioned in.

    Parameters:
    - pos: a tuple of the x,y-coordinates of the user's mouse location.

    Returns:
    - Returns the row and column of where the user's mouse is positioned as a tuple.

    Preconditions:
    - pos is within the size of the screen.
    """
    x, y = pos
    row = y // constants.SQUARE_SIZE
    col = x // constants.SQUARE_SIZE
    return (row, col)


def game_over(screen: pygame.Surface, winner: tuple[int, int, int], board: list[list[Piece | int]]) -> None:
    """ screen for when game ends

    Parameters:
    - screen: the pygame screen object.
    - winner: the colour of the winning player.
    - board: the end result of the finished game of checkers.

    Preconditions:
    - screen is a valid pygame surface object
    - winner in ((255, 255, 255), (0, 0, 0))
    - board is a valid game board
    """
    corbel_70 = pygame.font.SysFont('Corbel', 70)
    corbel_35 = pygame.font.SysFont('Corbel', 35)
    cont = True

    # Writing winner text
    if winner == (0, 0, 0):
        win_txt = corbel_70.render('BLACK WINS!', True, constants.BLACK)
    else:
        win_txt = corbel_70.render('WHITE WINS!', True, constants.WHITE)
    draw_game_over(screen, board)

    # Constructing buttons
    play_again_txt = corbel_35.render('Play Again?', True, constants.BLACK)
    quit_txt = corbel_35.render('QUIT', True, constants.BLACK)

    win_rect = win_txt.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 2))
    play_again_rect = play_again_txt.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 1.6))
    quit_rect = quit_txt.get_rect(center=(constants.WIDTH / 2, constants.HEIGHT / 1.5))

    screen.blit(win_txt, win_rect)

    while cont:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and play_again_rect.left <= x <= play_again_rect.right and \
                    play_again_rect.top <= y <= play_again_rect.bottom:
                main()

            elif event.type == pygame.MOUSEBUTTONDOWN and quit_rect.left <= x <= quit_rect.right and \
                    quit_rect.top <= y <= quit_rect.bottom:
                cont = False

        if play_again_rect.left <= x <= play_again_rect.right and play_again_rect.top <= y <= play_again_rect.bottom:
            pygame.draw.rect(
                surface=screen,
                color=constants.DARK_GREY,
                rect=[
                    play_again_rect.left,
                    play_again_rect.top,
                    play_again_rect.right - play_again_rect.left,
                    play_again_rect.bottom - play_again_rect.top
                ]
            )
        elif quit_rect.left <= x <= quit_rect.right and quit_rect.top <= y <= quit_rect.bottom:
            pygame.draw.rect(
                surface=screen,
                color=constants.DARK_GREY,
                rect=[
                    quit_rect.left,
                    quit_rect.top,
                    quit_rect.right - quit_rect.left,
                    quit_rect.bottom - quit_rect.top
                ]
            )
        else:
            pygame.draw.rect(
                surface=screen,
                color=constants.GREY,
                rect=[
                    play_again_rect.left,
                    play_again_rect.top,
                    play_again_rect.right - play_again_rect.left,
                    play_again_rect.bottom - play_again_rect.top
                ]
            )
            pygame.draw.rect(
                surface=screen,
                color=constants.GREY,
                rect=[
                    quit_rect.left,
                    quit_rect.top,
                    quit_rect.right - quit_rect.left,
                    quit_rect.bottom - quit_rect.top
                ]
            )

        screen.blit(play_again_txt, play_again_rect)
        screen.blit(quit_txt, quit_rect)

        pygame.display.update()


def draw_game_over(screen: pygame.Surface, board: list[list[Piece | int]]) -> None:
    """ Draws the game over screen

    Parameters:
    - screen: a pygame surface object in which the screen is drawn on.
    - board: the end result of the gameboard when the game ended.

    Preconditions:
    - screen is a valid pygame surface object.
    - board is valid game board.
    """
    screen.fill(constants.DARK_BROWN2)
    for row in range(constants.ROWS):
        for col in range(row % 2, constants.ROWS, 2):
            pygame.draw.rect(screen, constants.LIGHT_BROWN2, (
                col * constants.SQUARE_SIZE, row * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))
    for row in range(constants.ROWS):
        for col in range(constants.COLS):
            piece = board[row][col]
            if piece != 0:
                piece.draw(screen)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    main()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'constants', 'game', 'piece', 'ai', 'gametree'],
        'max-line-length': 120,
        'disable': ['no-member']  # python-ta did not recognise members of pygame
    })
