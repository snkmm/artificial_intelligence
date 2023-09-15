############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
import copy

############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    f = math.factorial
    return f(n ** 2) // f(n) // f(n * (n - 1))

def num_placements_one_per_row(n):
    return n ** n

def n_queens_valid(board):
    len_board = len(board)
    if (len_board != len(set(board))):
        return False
    for j in range(len_board):
        for i in range(1, len_board - j):
            if ((board[j] == board[i + j] - i) or
                (board[j] == board[i + j] + i)):
                return False
    return True

def n_queens_helper(n, board):
    for i in range(n):
        board.append(i)
        if (n_queens_valid(board)):
            yield board
        board.pop()

def n_queens_solutions_generator(n):
    stack = []
    stack.append(n_queens_helper(n, []))
    while stack:
        #Python review: Generators and exceptions, page 76
        try:
            board = copy.deepcopy(stack[len(stack) - 1].__next__())
        except:
            stack.pop()
            continue
        if (len(board) == n):
            yield board
        stack.append(n_queens_helper(n, board))

def n_queens_solutions(n):
    return list(n_queens_solutions_generator(n))

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.nrows = len(board)
        self.ncols = len(board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.get_board()[row][col] = not self.get_board()[row][col]
        if (row > 0):
            self.get_board()[row - 1][col] = not self.get_board()[row - 1][col]
        if (row < len(self.get_board()) - 1):
            self.get_board()[row + 1][col] = not self.get_board()[row + 1][col]
        if (col > 0):
            self.get_board()[row][col - 1] = not self.get_board()[row][col - 1]
        if (col < len(self.get_board()[0]) - 1):
            self.get_board()[row][col + 1] = not self.get_board()[row][col + 1]

    def scramble(self):
        for col in range(self.ncols):
            for row in range(self.nrows):
                if (random.random() < 0.5):
                    self.perform_move(row, col)

    def is_solved(self):
        for col in range(self.ncols):
            for row in range(self.nrows):
                if (self.board[row][col]):
                    return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield ((row, col), new_puzzle)

    def find_helper(self):
        #Python review: List, Dictionary, Set Comprehensions, pages 59 - 63
        return tuple(tuple(i) for i in self.get_board())

    def find_solution(self):
        sol = []
        frontier = [self]
        reached = {}
        while frontier:
            p = frontier.pop(0)
            for move, new_p in p.successors():
                s = new_p.find_helper()
                if (s not in reached):
                    reached[s] = [move]
                    if (new_p.is_solved()):
                        while (new_p.board != self.get_board()):
                            s = new_p.find_helper()
                            sol = reached[s] + sol
                            new_p.perform_move(sol[0][0], sol[0][1])
                        return sol
                else:
                    continue
                frontier.append(new_p)
        return None

def create_puzzle(rows, cols):
    result = []
    for _ in range(rows):
        result.append([False for _ in range(cols)])
    return LightsOutPuzzle(result)

############################################################
# Section 3: Linear Disk Movement
############################################################

class LinearDiskMovement(object):

    def __init__(self, length, n):
        self.length = length
        self.n = n

    def copy(self, n):
        return list(copy.deepcopy(n))

    def perform_move(self, length, n):
        new_rows = []
        for i, x in enumerate(n):
            if (i > 0):
                if (n[i - 1] == None):
                    row = self.copy(n)
                    row[i], row[i - 1] = None, x
                    new_rows.append(((i, i - 1), tuple(row)))
            if (i < length - 1):
                if (n[i + 1] == None):
                    row = self.copy(n)
                    row[i], row[i + 1] = None, x
                    new_rows.append(((i, i + 1), tuple(row)))
            if (i > 1):
                if ((n[i - 2] == None) and (n[i - 1] != None)):
                    row = self.copy(n)
                    row[i], row[i - 2] = None, x
                    new_rows.append(((i, i - 2), tuple(row)))
            if (i < length - 2):
                if ((n[i + 2] == None) and (n[i + 1] != None)):
                    row = self.copy(n)
                    row[i], row[i + 2] = None, x
                    new_rows.append(((i, i + 2), tuple(row)))
        return new_rows

    def find_helper(self, identical):
        result = []
        for i in range(self.length):
            if (i < self.n):
                if (identical):
                    result.append(0)
                else:
                    result.append(i)
            else:
                result.append(None)
        return tuple(result)

    def find_solution(self, identical=True):
        node = self.find_helper(identical)
        frontier = [node]
        reached = {}
        reached[node] = []
        goal = node[::-1]
        while frontier:
            p = frontier.pop(0)
            if (goal == p):
                return reached[p]
            p_successors = self.perform_move(self.length, p)
            for move, new_p in p_successors:
                s = new_p
                if (s not in reached):
                    reached[s] = reached[p] + [move]
                    frontier.append(s)

def solve_identical_disks(length, n):
    return LinearDiskMovement(length, n).find_solution()

def solve_distinct_disks(length, n):
    return LinearDiskMovement(length, n).find_solution(False)