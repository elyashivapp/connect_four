import numpy as np


def count_pieces(board, player):
    pieces = 0
    for row in range(6):
        for col in range(7):
            if board[row][col] == player:
                pieces += 1
    return pieces


def count_threes(board, player):
    threes = 0
    # check horizontally
    for row in range(6):
        for col in range(4):
            if board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == player and \
                    board[row][col + 3] == 0:
                threes += 1
            elif board[row][col] == 0 and board[row][col + 1] == player and board[row][col + 2] == player and \
                    board[row][col + 3] == player:
                threes += 1
            elif board[row][col] == player and board[row][col + 1] == 0 and board[row][col + 2] == player and \
                    board[row][col + 3] == player:
                threes += 1
            elif board[row][col] == player and board[row][col + 1] == player and board[row][col + 2] == 0 and \
                    board[row][col + 3] == player:
                threes += 1

    # check vertically
    for row in range(3):
        for col in range(7):
            if board[row][col] == player and board[row + 1][col] == player and board[row + 2][col] == player and \
                    board[row + 3][col] == 0:
                threes += 1

    # check diagonally from top left to bottom right
    for row in range(3):
        for col in range(4):
            if board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and \
                    board[row + 3][col + 3] == 0:
                threes += 1
            elif board[row][col] == 0 and board[row + 1][col + 1] == player and board[row + 2][col + 2] == player and \
                    board[row + 3][col + 3] == player:
                threes += 1
            elif board[row][col] == player and board[row + 1][col + 1] == 0 and board[row + 2][col + 2] == player and \
                    board[row + 3][col + 3] == player:
                threes += 1
            elif board[row][col] == player and board[row + 1][col + 1] == player and board[row + 2][col + 2] == 0 and \
                    board[row + 3][col + 3] == player:
                threes += 1

    # check diagonally from top right to bottom left
    for row in range(3):
        for col in range(3, 7):
            if board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and \
                    board[row + 3][col - 3] == 0:
                threes += 1
            elif board[row][col] == 0 and board[row + 1][col - 1] == player and board[row + 2][col - 2] == player and \
                    board[row + 3][col - 3] == player:
                threes += 1
            elif board[row][col] == player and board[row + 1][col - 1] == 0 and board[row + 2][col - 2] == player and \
                    board[row + 3][col - 3] == player:
                threes += 1
            elif board[row][col] == player and board[row + 1][col - 1] == player and board[row + 2][col - 2] == 0 and \
                    board[row + 3][col - 3] == player:
                threes += 1

    return threes


class Cpu:

    def __init__(self, player, depth, board=np.zeros((6, 7))):
        self.board = board.copy()
        self.player = player
        self.depth = depth
        self.forth_list = []
        self._row = len(self.board)
        self._column = len(self.board[0, :])

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
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece \
                        and self.board[r + 3][c + 3] == piece:
                    return True

        for c in range(self._column - 3):
            for r in range(3, self._row):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece \
                        and self.board[r - 3][c + 3] == piece:
                    return True

        return False

    def evaluate(self):
        # evaluation score
        win_score = 100000  # Score for a winning position
        two_in_a_row_score = 10  # Score for having two pieces in a row
        one_in_a_row_score = 1  # Score for having one pieces in a row

        # check for wins
        if self.winning_move(self.player):
            return win_score
        elif self.winning_move(3 - self.player):
            return -win_score

        # evaluate the number of threes for each player
        threes_you = count_threes(self.board, self.player)
        threes_rival = count_threes(self.board, 3 - self.player)

        # calculate the evaluation score
        score = threes_you * two_in_a_row_score - threes_rival * two_in_a_row_score

        # evaluate the number of one pieces for each player
        pieces_you = count_pieces(self.board, self.player)
        pieces_rival = count_pieces(self.board, 3 - self.player)

        score += pieces_you * one_in_a_row_score - pieces_rival * one_in_a_row_score

        return score

    # placing the piece in the right spot
    def drop(self, col, player):
        row = self.get_next_open_row(col)
        self.board[row][col] = player

    # displacing the piece
    def undrop(self, col):
        if self.is_valid_location(col):
            row = self.get_next_open_row(col)
            self.board[row - 1][col] = 0
        else:
            self.board[5][col] = 0

    # checking to see if the chosen location is available
    def is_valid_location(self, col):
        return self.board[self._row - 1][col] == 0

    # checking for possible moves, returns a list of them
    def get_possible_moves(self):
        possible_move_list = []
        for c in range(7):
            if self.is_valid_location(c):
                possible_move_list.append(c)
        return possible_move_list

    # make the piece fall in the right row
    def get_next_open_row(self, col):
        for i in range(self._row):
            if self.board[i][col] == 0:
                return i

    # the min-max alphabeta algorithm
    def alphabeta(self, depth, alpha, beta, maximizing_player):
        # recursive end
        if depth == 0 or self.game_over():
            return self.evaluate()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves():
                self.drop(move, self.player)
                board_evaluation = self.alphabeta(depth - 1, alpha, beta, False)
                self.undrop(move)
                max_eval = max(max_eval, board_evaluation)
                alpha = max(alpha, board_evaluation)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves():
                self.drop(move, 3 - self.player)
                board_evaluation = self.alphabeta(depth - 1, alpha, beta, True)
                self.undrop(move)
                min_eval = min(min_eval, board_evaluation)
                beta = min(beta, board_evaluation)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self):
        # checking for a winning move
        win = self.immediate_win()
        if win != -1:
            return win
        # checking if the rival can win next move, instead of wasting time using the algorithm
        danger = self.immediate_danger()
        if danger != -1:
            return danger
        best_eval = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        for move in self.get_possible_moves():
            self.drop(move, self.player)
            board_evaluation = self.alphabeta(self.depth - 1, alpha, beta, False)
            self.undrop(move)
            if board_evaluation > best_eval:
                best_eval = board_evaluation
                best_move = move
            alpha = max(alpha, board_evaluation)
        return best_move

    def immediate_danger(self):
        for move in self.get_possible_moves():
            self.drop(move, 3 - self.player)
            if self.winning_move(3 - self.player):
                self.undrop(move)
                return move
            self.undrop(move)
        return -1

    def immediate_win(self):
        for move in self.get_possible_moves():
            self.drop(move, self.player)
            if self.winning_move(self.player):
                self.undrop(move)
                return move
            self.undrop(move)
        return -1



def main():
    b = np.zeros((6, 7))
    c1 = Cpu(1, b)
    c2 = Cpu(2, b)
    x = 0

    while not c2.game_over():
        m1 = c1.get_best_move(7)
        print(m1)
        c1.drop(m1, 1)
        c2.drop(m1, 1)
        # m2 = c2.get_best_move(c2.board, 5)
        if c2.game_over():
            break
        while True:
            m2 = int(input(":"))
            if c2.is_valid_location(m2):
                break
            print("try again")
        print(m2)
        c1.drop(m2, 2)
        c2.drop(m2, 2)
        x += 1
        print(np.flip(c1.board, 0))


if __name__ == "__main__":
    main()
