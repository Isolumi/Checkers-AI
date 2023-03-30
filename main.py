import pygame
from checkers.constants import *
from checkers.game import Game
import sys
from checkers.piece import Piece

FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers!')
pygame.init()


def get_row_col_from_mouse(pos: tuple[int, int]) -> tuple:
    """ returns the square corresponding to the user's mouse position """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return (row, col)


def main() -> None:
    """ main function where the game is run """
    run = True
    clock = pygame.time.Clock()
    game = Game(SCREEN)
    winner = ()

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            winner = game.winner()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    game_over(SCREEN, winner[0], winner[1])


def game_over(screen: pygame.Surface, winner: tuple[int, int, int], board: list[list[Piece | int]]) -> None:
    """ screen for when game ends """
    corbel_70 = pygame.font.SysFont('Corbel', 70)
    corbel_35 = pygame.font.SysFont('Corbel', 35)
    cont = True

    # Writing winner text
    if winner == (0, 0, 0):
        win_txt = corbel_70.render('BLACK WINS!', True, BLACK)
    else:
        win_txt = corbel_70.render('WHITE WINS!', True, WHITE)
    draw_game_over(screen, winner, board)

    # Constructing buttons
    play_again_txt = corbel_35.render('Player Again?', True, BLACK)
    quit_txt = corbel_35.render('QUIT', True, BLACK)

    win_rect = win_txt.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    play_again_rect = play_again_txt.get_rect(center=(WIDTH / 2, HEIGHT / 1.6))
    quit_rect = quit_txt.get_rect(center=(WIDTH / 2, HEIGHT / 1.5))

    screen.blit(win_txt, win_rect)

    while cont:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.left <= x <= play_again_rect.right and \
                        play_again_rect.top <= y <= play_again_rect.bottom:
                    main()
                elif quit_rect.left <= x <= quit_rect.right and quit_rect.top <= y <= quit_rect.bottom:
                    pygame.quit()

        if play_again_rect.left <= x <= play_again_rect.right and play_again_rect.top <= y <= play_again_rect.bottom:
            pygame.draw.rect(
                surface=screen,
                color=BLUE,
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
                color=BLUE,
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
                color=GREY,
                rect=[
                    play_again_rect.left,
                    play_again_rect.top,
                    play_again_rect.right - play_again_rect.left,
                    play_again_rect.bottom - play_again_rect.top
                ]
            )
            pygame.draw.rect(
                surface=screen,
                color=GREY,
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
    screen.fill(DARK_BROWN2)
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(screen, LIGHT_BROWN2, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != 0:
                piece.draw(screen)


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)

    main()

    # import python_ta
    # python_ta.check_all(config={
    #     'max-line-length': 120
    # })
