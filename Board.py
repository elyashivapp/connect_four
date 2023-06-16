import numpy as np


# the board class
class Board:

    def __init__(self, board=np.zeros((6, 7))):
        self.turn = 1
        self.board = board
        self.last_move_list = []
        self._row = len(board)
        self._column = len(board[0])

    def __str__(self):
        return str(np.flip(self.board, 0))

    # placing the piece in the right spot
    def drop(self, col):
        row = self.get_next_open_row(col)
        self.board[row][col] = self.turn
        self.turn = 3 - self.turn
        self.last_move_list.insert(0, col)

    # displacing the piece
    def undrop(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.board[row - 1][col] = 0
        else:
            self.board[5][col] = 0
        self.turn = 3 - self.turn

    # func to return last move
    def last_move(self):
        return self.last_move_list[0]

    # checking to see if the chosen location is available
    def is_valid_location(self, col):
        return self.board[self._row - 1][col] == 0

    # make the piece fall in the right row
    def get_next_open_row(self, col):
        for i in range(self._row):
            if self.board[i][col] == 0:
                return i

    # checking for possible moves, returns a list of them
    def get_possible_moves(self):
        possible_move_list = []
        for c in range(7):
            if self.is_valid_location(c):
                possible_move_list.append(c)
        return possible_move_list

    # checking if the chosen move is the winning move
    # the function is going through every possible winning situation
    def winning_move(self, piece):
        for c in range(self._column - 3):
            for r in range(self._row):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece \
                        and self.board[r][c + 3] == piece:
                    return True

        for c in range(self._column):
            for r in range(self._row - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece \
                        and self.board[r + 3][c] == piece:
                    return True

        for c in range(self._column - 3):
            for r in range(self._row - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                    c + 2] == piece \
                        and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self._column - 3):
            for r in range(3, self._row):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                    c + 2] == piece \
                        and self.board[r - 3][c + 3] == piece:
                    return True

        return False

    # check all possible game ending situations
    def game_over(self):
        for c in range(self._column - 3):
            for r in range(self._row):
                if self.board[r][c] == self.board[r][c + 1] == self.board[r][c + 2] == self.board[r][c + 3] != 0:
                    return True

        for c in range(self._column):
            for r in range(self._row - 3):
                if self.board[r][c] == self.board[r + 1][c] == self.board[r + 2][c] == self.board[r + 3][c] != 0:
                    return True

        for c in range(self._column - 3):
            for r in range(self._row - 3):
                if self.board[r][c] == self.board[r + 1][c + 1] == self.board[r + 2][c + 2] == self.board[r + 3][
                    c + 3] != 0:
                    return True

        for c in range(self._column - 3):
            for r in range(3, self._row):
                if self.board[r][c] == self.board[r - 1][c + 1] == self.board[r - 2][c + 2] == self.board[r - 3][
                    c + 3] != 0:
                    return True

        return self.board.all()
