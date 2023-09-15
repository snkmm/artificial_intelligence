############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import collections
import copy
import itertools
import random
import math

############################################################
# Section 1: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    result = [[False for _ in range(cols)] for _ in range(rows)]
    return DominoesGame(result)

class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.nrows = len(board)
        self.ncols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        result = [[False for _ in range(self.ncols)] for _ in range(self.nrows)]
        self.board = result

    def is_legal_move(self, row, col, vertical):
        if ((row < 0) or (row > self.nrows - 1) or (col < 0) or (col > self.ncols - 1)):
            return False
        if (vertical):
            if (row == self.nrows - 1):
                return False
            if ((self.get_board()[row][col]) or (self.get_board()[row + 1][col])):
                return False
        else:
            if (col == self.ncols - 1):
                return False
            if ((self.get_board()[row][col]) or (self.get_board()[row][col + 1])):
                return False
        return True

    def legal_moves(self, vertical):
        for row in range(self.nrows):
            for col in range(self.ncols):
                if (self.is_legal_move(row, col, vertical)):
                    yield (row, col)

    def perform_move(self, row, col, vertical):
        self.get_board()[row][col] = True
        if (vertical):
            self.get_board()[row + 1][col] = True
        else:
            self.get_board()[row][col + 1] = True

    def game_over(self, vertical):
        if (len(list(self.legal_moves(vertical)))):
            return False
        return True

    def copy(self):
        result = [self.board[i][:] for i in range(self.nrows)]
        return DominoesGame(result)

    def successors(self, vertical):
        for row, col in self.legal_moves(vertical):
            new_puzzle = self.copy()
            new_puzzle.perform_move(row, col, vertical)
            yield ((row, col), new_puzzle)

    def get_random_move(self, vertical):
        seq = list(self.legal_moves(vertical))
        return random.choice(seq)

    def max_value(self, vertical, limit, alpha, beta):
        if ((limit == 0) or (self.game_over(vertical))):
            v_y = list(self.legal_moves(vertical))
            v_n = list(self.legal_moves(not vertical))
            return len(v_y) - len(v_n), None, 1
        v = -math.inf
        mover, count = None, 0
        for move, new_p in self.successors(vertical):
            v2, a2, cnt = new_p.min_value(vertical, limit - 1, alpha, beta)
            count += cnt
            if (v2 > v):
                v, mover = v2, move
                alpha = max(alpha, v)
            if (v >= beta):
                return v, mover, count
        return v, mover, count

    def min_value(self, vertical, limit, alpha, beta):
        no_vertical = not vertical
        if ((limit == 0) or (self.game_over(no_vertical))):
            v_y = list(self.legal_moves(vertical))
            v_n = list(self.legal_moves(no_vertical))
            return len(v_y) - len(v_n), None, 1
        v = math.inf
        mover, count = None, 0
        for move, new_p in self.successors(no_vertical):
            v2, a2, cnt = new_p.max_value(vertical, limit - 1, alpha, beta)
            count += cnt
            if (v2 < v):
                v, mover = v2, move
                beta = min(beta, v)
            if (v <= alpha):
                return v, mover, count
        return v, mover, count

    # Required
    def get_best_move(self, vertical, limit):
        result = self.max_value(vertical, limit, -math.inf, math.inf)
        return result[1], result[0], result[2]