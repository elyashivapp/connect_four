import random
import sys
import time
from threading import Thread
import numpy as np
import pygame
import math

# colors
BLACK = "black"
BLUE = "blue"
GREEN = "#15d642"
RED = "#e03409"


class ConnectFour2:

    # constructor and building the board
    def __init__(self):
        self._player = 2
        self._font = None
        self.screen = None  # to be changed later
        self.turn = 1
        self.game_over = False
        self.last_move_list = []
        self._square_size = 100
        self._row_count = 6
        self._column_count = 7
        self._width = self._column_count * self._square_size
        self._height = (self._row_count + 1) * self._square_size
        self.board = np.zeros((self._row_count, self._column_count))

    def __str__(self):
        return str(np.flip(self.board, 0))

    # is it my turn
    def is_my_turn(self):
        return self._player == self.turn

    # a part that's happening twice during the animation function
    def help_animation(self, col, i):
        pygame.display.update()
        pygame.time.wait(70)
        pygame.draw.circle(self.screen, BLACK, (int((col + 0.5) * self._square_size),
                                                int((i + 1.5) * self._square_size)), 45)
        pygame.display.update()

    # making the illusion of the piece dropping
    def animation(self, col):
        for i in range(self._row_count):
            if self.board[self._row_count - 1 - i, col] == 0:
                if self.turn == 1:
                    pygame.draw.circle(self.screen, GREEN, (int((col + 0.5) * self._square_size),
                                                            int((i + 1.5) * self._square_size)), 45)
                    self.help_animation(col, i)
                else:
                    pygame.draw.circle(self.screen, RED, (int((col + 0.5) * self._square_size),
                                                          int((i + 1.5) * self._square_size)), 45)
                    self.help_animation(col, i)

    # following the mouse animation
    def follow(self, event):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
        posx = event.pos[0]
        if self.turn == 1:
            pygame.draw.circle(self.screen, GREEN, (posx, int(self._square_size / 2)), 45)
        else:
            pygame.draw.circle(self.screen, RED, (posx, int(self._square_size / 2)), 45)

    # placing the piece in the right spot
    def drop(self, col):
        row = self.get_next_open_row(col)
        self.animation(col)
        self.board[row][col] = self.turn
        self.current_board()
        self.turn = 3 - self.turn
        self.last_move_list.insert(0, col)

    # func to return last move
    def last_move(self):
        return self.last_move_list[0]

    # checking to see if the chosen location is available
    def is_valid_location(self, col):
        return self.board[self._row_count - 1][col] == 0

    # make the piece fall in the right row
    def get_next_open_row(self, col):
        for i in range(self._row_count):
            if self.board[i][col] == 0:
                return i

    # checking if the chosen move is the winning move
    # the function is going through every possible winning situation
    def winning_move(self, piece):
        for c in range(self._column_count - 3):
            for r in range(self._row_count):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece \
                        and self.board[r][c + 3] == piece:
                    return True

        for c in range(self._column_count):
            for r in range(self._row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece \
                        and self.board[r + 3][c] == piece:
                    return True

        for c in range(self._column_count - 3):
            for r in range(self._row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece \
                        and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self._column_count - 3):
            for r in range(3, self._row_count):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece \
                        and self.board[r - 3][c + 3] == piece:
                    return True

        return False

    # a function to draw the board on the pygame window
    def draw_board(self):
        for c in range(self._column_count):
            for r in range(self._row_count):
                pygame.draw.rect(self.screen, BLUE, (
                    c * self._square_size, (r + 1) * self._square_size, self._square_size, self._square_size))
                pygame.draw.circle(self.screen, BLACK,
                                   (int((c + 0.5) * self._square_size), int((r + 1.5) * self._square_size)), 45)

    # a function to make the current board
    def current_board(self):
        for c in range(self._column_count):
            for r in range(self._row_count):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, GREEN,
                                       (int((c + 0.5) * self._square_size),
                                        self._height - int((r + 0.5) * self._square_size)), 45)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, RED,
                                       (int((c + 0.5) * self._square_size),
                                        self._height - int((r + 0.5) * self._square_size)), 45)
        pygame.display.update()

    # resetting
    def reset(self):
        self.turn = 1
        pygame.time.wait(3000)
        self.game_over = False
        self.draw_board()
        for c in range(self._column_count):
            for r in range(self._row_count):
                self.board[r][c] = 0

    # the game setting
    def setting_game(self):
        pygame.init()
        pygame.display.set_caption("connect four")
        self._font = pygame.font.SysFont("monospace", 45)

        self.screen = pygame.display.set_mode((self._width, self._height))
        self.draw_board()
        pygame.display.update()

    # the game
    def game(self):
        self.setting_game()
        while not self.game_over:

            # pressing x
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # in a case of tie
                if self.board.all():
                    self.current_board()
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
                    label = self._font.render("Tie, no one won.", 1, "white")
                    self.screen.blit(label, (40, 10))
                    self.game_over = True

                # following the mouse animation
                if event.type == pygame.MOUSEMOTION:
                    self.follow(event)
                pygame.display.update()

                # the playing part
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # checking which player's turn is it
                    if self.turn == 1:
                        posx = event.pos[0]
                        col1 = int(math.floor(posx / self._square_size))
                        if self.is_valid_location(col1):
                            self.drop(col1)

                            if self.winning_move(1):
                                self.current_board()
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
                                label = self._font.render("The Green Player Won!!!", 1, GREEN)
                                self.screen.blit(label, (40, 10))
                                self.game_over = True

                        else:
                            self.turn == 1
                    # end of the green player's turn

                    # red player
                    elif self.turn == 2:
                        posx = event.pos[0]
                        col2 = int(math.floor(posx / self._square_size))

                        if self.is_valid_location(col2):
                            self.drop(col2)

                            if self.winning_move(2):
                                self.current_board()
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
                                label2 = self._font.render("The Red Player Won!!!", 1, RED)
                                self.screen.blit(label2, (40, 10))
                                self.game_over = True

                        else:
                            self.turn = 2
                    # end of the red player's turn

                    print(self)
                    self.current_board()

                # resetting the game
                if self.game_over:
                    self.reset()


def start_game(c):
    c.game()


def play_vs_random():
    random.randint(0, 6)
    c = ConnectFour2()
    start_game_thread = Thread(target=lambda: start_game(c))
    start_game_thread.start()
    while True:
        while True:
            if not c.is_my_turn():
                break
            time.sleep(0.5)
        c.drop(random.randint(0, 6))


def main():
    pass


if __name__ == "__main__":
    main()
