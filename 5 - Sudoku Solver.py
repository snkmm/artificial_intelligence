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
# Sudoku Solver
############################################################

def sudoku_cells():
    return [(row, col) for row in range(9) for col in range(9)]

def sudoku_arcs():
    arcs = set()
    for r1, c1 in sudoku_cells():
        for r2, c2 in sudoku_cells():
            if ((r1, c1) != (r2, c2)):
                if ((r1 == r2) or
                    (c1 == c2) or
                    (r1 // 3 == r2 // 3 and c1 // 3 == c2 // 3)):
                    arcs.add(((r1, c1), (r2, c2)))
    return arcs

def read_board(path):
    board = dict()
    f = open(path)
    lines = f.readlines()
    for row, line in enumerate(lines):
        for col, lst in enumerate(list(line)[:9]):
            if (lst == "*"):
                board[(row, col)] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                board[(row, col)] = set([int(lst)])
    f.close()
    return board

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if (len(self.get_values(cell2)) != 1):
            return False
        c2 = next(iter(self.get_values(cell2)))
        if (c2 in self.get_values(cell1)):
            self.get_values(cell1).remove(c2)
            return True
        return False

    def neighbors(self, cell):
        return set(j for (i, j) in Sudoku.ARCS if i == cell)

    def infer_ac3(self):
        queue = sudoku_arcs()
        while queue:
            (X_i, X_j) = queue.pop()
            if (self.remove_inconsistent_values(X_i, X_j)):
                for X_k in (self.neighbors(X_i) - {X_j}):
                    queue.add((X_k, X_i))

    def infer_improved(self):
        made_additional_inferences = True
        while made_additional_inferences:
            self.infer_ac3()
            made_additional_inferences = False
            for cell in Sudoku.CELLS:
                if (len(self.get_values(cell)) != 1):
                    c = set()
                    for i in range(9):
                        if (i != cell[0]):
                            c = self.get_values((i, cell[1])) | c
                        elif (i != cell[1]):
                            c = self.get_values((cell[0], i)) | c
                    if (len(self.get_values(cell) - c) == 1):
                        made_additional_inferences = True
                        self.board[cell] = self.get_values(cell) - c

    def is_solved(self):
        for cell in Sudoku.CELLS:
            if (len(self.get_values(cell)) != 1):
                return False
        return True

    def infer_with_guessing(self):
        self.infer_improved()
        for cell in Sudoku.CELLS:
            if (len(self.get_values(cell)) != 1):
                for c in self.get_values(cell):
                    current_board = copy.deepcopy(self.board)
                    self.board[cell] = set([c])
                    self.infer_with_guessing()
                    if self.is_solved():
                        break
                    else:
                        self.board = copy.deepcopy(current_board)