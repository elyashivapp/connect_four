import random
import socket
import sys
import time
from threading import Thread
import numpy as np
import rsa
import pygame
import math

# colors
BLACK = "black"
BLUE = "blue"
GREEN = "#15d642"
RED = "#e03409"
WHITE = "white"

players = {1: "Green", 2: "Red"}
players_colors = {1: GREEN, 2: RED}

IP = "127.0.0.1"
PORT = 8789


class ConnectFour2:

    # constructor and building the board
    def __init__(self, player=1):
        self._player = player
        self._font = None  #
        self.screen = None  # to be changed later
        self.turn = 1
        self.game_over = False
        self.you_played_finishing = False
        self.finished_1 = False  # for signaling to the other thread to continue
        self.finished_2 = False
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
        if self._player == 1:
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
        self.last_move_list = []
        self.draw_board()
        self.board = np.zeros((self._row_count, self._column_count))
        self.current_board()
        self.finished_2 = True
        while True:
            if self.finished_1:
                self.finished_1 = False
                break
            time.sleep(0.5)
        self.you_played_finishing = False
        self.game()

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
        self.game_over = False
        while not self.game_over:

            for event in pygame.event.get():
                # pressing x
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # in a case of tie
                if self.board.all():
                    self.current_board()
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
                    label = self._font.render("Tie, no one won.", 1, WHITE)
                    self.screen.blit(label, (40, 10))
                    self.game_over = True
                    self.you_played_finishing = True
                    time.sleep(2)
                    while True:
                        if self.finished_1:
                            self.finished_1 = False
                            break
                        time.sleep(0.5)

                # following the mouse animation
                if event.type == pygame.MOUSEMOTION:
                    self.follow(event)
                pygame.display.update()

                # the playing part
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # your turn
                    if self.turn == self._player:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self._square_size))
                        if self.is_valid_location(col):
                            self.drop(col)

                            if self.winning_move(self._player):
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self._width, self._square_size))
                                label = self._font.render(f"The {players[self._player]} Player Won!!!", 1,
                                                          players_colors[self._player])
                                self.screen.blit(label, (40, 10))
                                self.game_over = True  # resetting the game
                                self.you_played_finishing = True
                                time.sleep(2)
                                while True:
                                    if self.finished_1:
                                        self.finished_1 = False
                                        break
                                    time.sleep(0.5)

                    # end of your turn

                    print(self)
                    self.current_board()

        self.reset()


def start_game(c):
    c.setting_game()
    c.game()


def waiting_screen(c):
    pygame.init()
    pygame.display.set_caption("waiting...")
    font = pygame.font.SysFont("monospace", 30)
    screen = pygame.display.set_mode((600, 80))
    screen.fill(WHITE)
    label = font.render("Waiting for second player...", 1, BLACK)
    screen.blit(label, (10, 10))
    pygame.display.update()
    while not c.finished_1:
        for event in pygame.event.get():
            # pressing x
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    c.finished_1 = False
    pygame.quit()


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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("server connected")
    which_player = int(client_socket.recv(1024).decode())
    c = ConnectFour2(which_player)
    if c._player == 1:
        waiting_screen_thread = Thread(target=lambda: waiting_screen(c))
        waiting_screen_thread.start()
        client_socket.recv(1024).decode()
        c.finished_1 = True
        while True:
            if not c.finished_1:
                break
            time.sleep(0.5)
        waiting_screen_thread.join()
    start_game_thread = Thread(target=lambda: start_game(c))
    start_game_thread.start()

    while True:
        # wait for move
        while True:
            if not c.is_my_turn():
                break
            time.sleep(0.5)

        # send your move to the server
        if c._player != 2 or len(c.last_move_list) >= 1:
            client_socket.send(str(c.last_move()).encode())

        # what to do if the game is over
        if c.game_over:
            c.finished_1 = True
            if c.you_played_finishing:
                while True:
                    if c.finished_2:
                        c.finished_2 = False
                        break
                    time.sleep(0.5)
                c.finished_1 = True
                if c._player == 1:
                    continue
            else:   # player 1 never gets here
                client_socket.send("done".encode())

        # get player-2's move from the server
        player_b_move = int(client_socket.recv(1024).decode())
        if 0 <= player_b_move <= 6:
            c.drop(player_b_move)
            # checks if the second player won
            if c.winning_move(3 - c._player):
                pygame.draw.rect(c.screen, BLACK, (0, 0, c._width, c._square_size))
                label = c._font.render(f"The {players[3 - c._player]} Player Won!!!", 1, players_colors[3 - c._player])
                c.screen.blit(label, (40, 10))
                c.game_over = True
                time.sleep(2)
                while True:
                    if c.finished_2:
                        c.finished_2 = False
                        break
                    time.sleep(0.5)
                if c._player == 1:
                    c.finished_1 = True
            # checks if second player played a tie
            elif c.board.all():
                pygame.draw.rect(c.screen, BLACK, (0, 0, c._width, c._square_size))
                label = c._font.render("Tie, no one won.", 1, WHITE)
                c.screen.blit(label, (40, 10))
                c.game_over = True
                time.sleep(2)
                while True:
                    if c.finished_2:
                        c.finished_2 = False
                        break
                    time.sleep(0.5)
                if c._player == 1:
                    c.finished_1 = True


        else:
            print("illegal move!")


if __name__ == "__main__":
    main()
