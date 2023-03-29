import pygame
from checkers.constants import *
from checkers.board import Board
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers!')

def get_row_col_from_mouse(pos: tuple[int, int]) -> tuple:
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return (row, col)


def main() -> None:
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    # winner decided, potetially do play again feature
    pygame.quit()


main()
