import socket
import sys
import time
from threading import Thread
import numpy as np
import random
import rsa
import tkinter as tk
import pygame
import math
from Board import Board
import cpu

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
public_key, private_key = rsa.newkeys(512)


class ConnectFour(Board):

    # constructor and building the board
    def __init__(self, player=1):
        super().__init__()
        self.player = player
        self.font = None  #
        self.screen = None  # to be changed later
        self.game_over = False
        self.you_played_finishing = False
        self.finished_1 = False  # for signaling to the other thread to continue
        self.finished_2 = False
        self.square_size = 100
        self.width = self._column * self.square_size
        self._height = (self._row + 1) * self.square_size

    def __str__(self):
        return str(np.flip(self.board, 0))

    # is it my turn
    def is_my_turn(self):
        return self.player == self.turn

    # a part that's happening twice during the animation function
    def help_animation(self, col, i):
        pygame.display.update()
        pygame.time.wait(70)
        pygame.draw.circle(self.screen, BLACK, (int((col + 0.5) * self.square_size),
                                                int((i + 1.5) * self.square_size)), 45)
        pygame.display.update()

    # making the illusion of the piece dropping
    def animation(self, col):
        for i in range(self._row):
            if self.board[self._row - 1 - i, col] == 0:
                if self.turn == 1:
                    pygame.draw.circle(self.screen, GREEN, (int((col + 0.5) * self.square_size),
                                                            int((i + 1.5) * self.square_size)), 45)
                    self.help_animation(col, i)
                else:
                    pygame.draw.circle(self.screen, RED, (int((col + 0.5) * self.square_size),
                                                          int((i + 1.5) * self.square_size)), 45)
                    self.help_animation(col, i)

    # following the mouse animation, not hotspot
    def follow(self, event):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
        posx = event.pos[0]
        if self.player == 1:
            pygame.draw.circle(self.screen, GREEN, (posx, int(self.square_size / 2)), 45)
        else:
            pygame.draw.circle(self.screen, RED, (posx, int(self.square_size / 2)), 45)

    # following in hotspot
    def follow_hotspot(self, event):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
        posx = event.pos[0]
        if self.turn == 1:
            pygame.draw.circle(self.screen, GREEN, (posx, int(self.square_size / 2)), 45)
        else:
            pygame.draw.circle(self.screen, RED, (posx, int(self.square_size / 2)), 45)

    # placing the piece in the right spot

    def drop(self, col):
        row = self.get_next_open_row(col)
        self.animation(col)
        self.board[row][col] = self.turn
        self.current_board()
        self.turn = 3 - self.turn
        self.last_move_list.insert(0, col)

    # a function to draw the board on the pygame window
    def draw_board(self):
        for c in range(self._column):
            for r in range(self._row):
                pygame.draw.rect(self.screen, BLUE, (
                    c * self.square_size, (r + 1) * self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, BLACK,
                                   (int((c + 0.5) * self.square_size), int((r + 1.5) * self.square_size)), 45)

    # a function to make the current board
    def current_board(self):
        for c in range(self._column):
            for r in range(self._row):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, GREEN,
                                       (int((c + 0.5) * self.square_size),
                                        self._height - int((r + 0.5) * self.square_size)), 45)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, RED,
                                       (int((c + 0.5) * self.square_size),
                                        self._height - int((r + 0.5) * self.square_size)), 45)
        pygame.display.update()

    # resetting
    def reset_online(self):
        self.turn = 1
        self.last_move_list = []
        self.draw_board()
        self.board = np.zeros((self._row, self._column))
        self.current_board()
        self.finished_2 = True
        while True:
            if self.finished_1:
                self.finished_1 = False
                break
            time.sleep(0.5)
        self.you_played_finishing = False
        self.game()

    def reset(self):
        self.turn = 1
        self.last_move_list = []
        self.board = np.zeros((self._row, self._column))

    # the game setting
    def setting_game(self):
        pygame.init()
        pygame.display.set_caption("connect four")
        self.font = pygame.font.SysFont("monospace", 45)

        self.screen = pygame.display.set_mode((self.width, self._height))
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
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                    label = self.font.render("Tie, no one won.", 1, WHITE)
                    self.screen.blit(label, (40, 10))
                    pygame.display.update()
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
                    if self.turn == self.player:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.square_size))
                        if self.is_valid_location(col):
                            self.drop(col)

                            if self.winning_move(self.player):
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                                label = self.font.render(f"The {players[self.player]} Player Won!!!", 1,
                                                         players_colors[self.player])
                                self.screen.blit(label, (40, 10))
                                pygame.display.update()
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

        self.reset_online()

    # play on the same machine
    def hotspot(self):
        self.setting_game()
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
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                    label = self.font.render("Tie, no one won.", 1, WHITE)
                    self.screen.blit(label, (40, 10))
                    pygame.display.update()
                    self.game_over = True
                    time.sleep(2)

                # following the mouse animation
                if event.type == pygame.MOUSEMOTION:
                    self.follow_hotspot(event)
                pygame.display.update()

                # the playing part
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Green turn
                    if self.turn == 1:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.square_size))
                        if self.is_valid_location(col):
                            self.drop(col)

                            if self.winning_move(1):
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                                label = self.font.render("The Green Player Won!!!", 1, GREEN)
                                self.screen.blit(label, (40, 10))
                                pygame.display.update()
                                self.game_over = True  # resetting the game
                                time.sleep(2)
                    # end of Greens turn

                    # Red turn
                    elif self.turn == 2:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.square_size))
                        if self.is_valid_location(col):
                            self.drop(col)

                            if self.winning_move(2):
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                                label = self.font.render("The Red Player Won!!!", 1, RED)
                                self.screen.blit(label, (40, 10))
                                pygame.display.update()
                                self.game_over = True  # resetting the game
                                time.sleep(2)
                    # end of Reds turn

                    print(self)
                    self.current_board()

        self.reset()
        pygame.quit()

    # vs the computer
    def cpu_game(self):
        self.setting_game()
        self.finished_1 = True
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
                    pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                    label = self.font.render("Tie, no one won.", 1, WHITE)
                    self.screen.blit(label, (40, 10))
                    pygame.display.update()
                    self.game_over = True
                    time.sleep(2)

                # following the mouse animation
                if event.type == pygame.MOUSEMOTION:
                    self.follow(event)
                pygame.display.update()

                # the playing part
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # your turn
                    if self.turn == self.player:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.square_size))
                        if self.is_valid_location(col):
                            self.drop(col)

                            if self.winning_move(self.player):
                                pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.square_size))
                                label = self.font.render(f"The {players[self.player]} Player Won!!!", 1,
                                                         players_colors[self.player])
                                self.screen.blit(label, (40, 10))
                                pygame.display.update()
                                time.sleep(2)
                                pygame.quit()
                            self.finished_1 = True
                    # end of your turn

                    print(self)
                    self.current_board()

        while True:
            if self.finished_1:
                self.finished_1 = False
                break
            time.sleep(0.5)

        self.reset()
        pygame.quit()


def encrypt(msg, pub_key):
    return rsa.encrypt(msg, pub_key)


def decrypt(msg, priv_key):
    return rsa.decrypt(msg, priv_key)


def start_game(c):
    c.setting_game()
    c.game()


def multi_command(window):
    window.destroy()
    multiplayer()


def hotspot_command(window):
    window.destroy()
    c = ConnectFour()
    c.hotspot()


def level_menu(old):
    old.destroy()
    window = tk.Tk()
    window.geometry("160x350")
    window.title("Choose level")
    window.resizable(False, False)
    hard_button = tk.Button(window, text="Hard", command=lambda: hard(window), width=10, height=2,
                            font=("Arial", 20),
                            background="#008cff")
    medium_button = tk.Button(window, text="Medium", command=lambda: medium(window), width=10, height=2,
                              font=("Arial", 20),
                              background="#008cff")
    easy_button = tk.Button(window, text="Easy", command=lambda: easy(window), width=10, height=2,
                            font=("Arial", 20),
                            background="#008cff")
    exit_button = tk.Button(window, text="Back", command=window.destroy, width=10, height=2, font=("Arial", 20),
                            background="red")
    easy_button.pack()
    medium_button.pack()
    hard_button.pack()
    exit_button.pack()
    window.mainloop()


def easy(window):
    window.destroy()
    cpu_command(2)


def medium(window):
    window.destroy()
    cpu_command(5)


def hard(window):
    window.destroy()
    cpu_command(7)


def cpu_command(depth):
    player = random.choice([1, 2])
    cpu_player = 3 - player
    game = ConnectFour(player)
    rival = cpu.Cpu(cpu_player, depth)
    cpu_game_thread = Thread(target=lambda: game.cpu_game())
    cpu_game_thread.start()

    while True:
        if game.finished_1:
            game.finished_1 = False
            break
        time.sleep(0.5)

    while not game.game_over:
        if game.turn == rival.player:
            if len(game.last_move_list) > 0:
                rival.drop(game.last_move())

            if len(game.last_move_list) < 2:
                game.drop(3)
                rival.drop(3)

            else:
                print(game.turn)
                move = rival.get_best_move()
                game.drop(move)
                rival.drop(move)

            if game.winning_move(cpu_player):
                pygame.draw.rect(game.screen, BLACK, (0, 0, game.width, game.square_size))
                label = game.font.render(f"The {players[rival.player]} Player Won!!!", 1,
                                         players_colors[rival.player])
                game.screen.blit(label, (40, 10))
                game.game_over = True
                time.sleep(2)
                game.finished_1 = True
        else:
            while True:
                if game.finished_1:
                    game.finished_1 = False
                    break
                time.sleep(0.5)

    cpu_game_thread.join()


def multiplayer():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    print("server connected")

    # get the server public key
    msg = client_socket.recv(1024)
    serv_pub_key = rsa.key.PublicKey.load_pkcs1(msg, format="DER")

    # send the server your public key
    client_socket.send(public_key.save_pkcs1(format="DER"))

    which_player = int(decrypt(client_socket.recv(1024), private_key))
    c = ConnectFour(which_player)

    if c.player == 1:
        waiting_screen_thread = Thread(target=lambda: waiting_screen(c))
        waiting_screen_thread.start()
        client_socket.recv(1024)
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
        if c.player != 2 or len(c.last_move_list) >= 1:
            client_socket.send(encrypt(str(c.last_move()).encode(), serv_pub_key))

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
                if c.player == 1:
                    continue
            else:  # player 1 never gets here
                client_socket.send(encrypt("done".encode(), serv_pub_key))

        # get player-2's move from the server
        player_b_move = int(decrypt(client_socket.recv(1024), private_key))
        if 0 <= player_b_move <= 6:
            c.drop(player_b_move)
            # checks if the second player won
            if c.winning_move(3 - c.player):
                pygame.draw.rect(c.screen, BLACK, (0, 0, c.width, c.square_size))
                label = c.font.render(f"The {players[3 - c.player]} Player Won!!!", 1, players_colors[3 - c.player])
                c.screen.blit(label, (40, 10))
                pygame.display.update()
                c.game_over = True
                time.sleep(2)
                while True:
                    if c.finished_2:
                        c.finished_2 = False
                        break
                    time.sleep(0.5)
                if c.player == 1:
                    c.finished_1 = True
            # checks if second player played a tie
            elif c.board.all():
                pygame.draw.rect(c.screen, BLACK, (0, 0, c.width, c.square_size))
                label = c.font.render("Tie, no one won.", 1, WHITE)
                c.screen.blit(label, (40, 10))
                pygame.display.update()
                c.game_over = True
                time.sleep(2)
                while True:
                    if c.finished_2:
                        c.finished_2 = False
                        break
                    time.sleep(0.5)
                if c.player == 1:
                    c.finished_1 = True

        else:
            print("illegal move!")


def waiting_screen(c):
    pygame.init()
    pygame.display.set_caption("waiting...")
    font = pygame.font.SysFont("monospace", 30)
    screen = pygame.display.set_mode((550, 80))
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


def main():
    # menu window
    window = tk.Tk()
    window.geometry("160x350")
    window.title("Connect Four Menu")
    window.resizable(False, False)
    window.protocol('WM_DELETE_WINDOW', sys.exit)
    hotspot_button = tk.Button(window, text="Hotspot", command=lambda: hotspot_command(window), width=10, height=2,
                               font=("Arial", 20),
                               background="#008cff")
    cpu_button = tk.Button(window, text="Cpu", command=lambda: level_menu(window), width=10, height=2,
                           font=("Arial", 20),
                           background="#008cff")
    multi_button = tk.Button(window, text="multiplayer", command=lambda: multi_command(window), width=10, height=2,
                             font=("Arial", 20),
                             background="#008cff")
    exit_button = tk.Button(window, text="Exit", command=sys.exit, width=10, height=2, font=("Arial", 20),
                            background="red")
    hotspot_button.pack()
    cpu_button.pack()
    multi_button.pack()
    exit_button.pack()
    window.mainloop()


if __name__ == "__main__":
    # calling the menu
    menu_on = True
    while menu_on:
        main()
