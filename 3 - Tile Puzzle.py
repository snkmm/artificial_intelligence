############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from queue import PriorityQueue
import random
import copy
import math

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    result = [[False for _ in range(cols)] for _ in range(rows)]
    number = 1
    for i in range(rows):
        for j in range(cols):
            result[i][j] = number
            number += 1
    result[rows - 1][cols - 1] = 0
    return TilePuzzle(result)

class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.nrows = len(board)
        self.ncols = len(board[0])
        self.empty = self.empty_tile()

    def get_board(self):
        return self.board

    def empty_tile(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                if (self.get_board()[row][col] == 0):
                    return row, col

    def perform_move(self, direction):
        row, col = self.empty
        if (direction == "up"):
            if (row <= 0):
                return False
            temp = self.get_board()[row - 1][col]
            self.get_board()[row - 1][col] = self.get_board()[row][col]
            self.get_board()[row][col] = temp
            self.empty = row - 1, col
            return True
        if (direction == "down"):
            if (row >= self.nrows - 1):
                return False
            temp = self.get_board()[row + 1][col]
            self.get_board()[row + 1][col] = self.get_board()[row][col]
            self.get_board()[row][col] = temp
            self.empty = row + 1, col
            return True
        if (direction == "left"):
            if (col <= 0):
                return False
            temp = self.get_board()[row][col - 1]
            self.get_board()[row][col - 1] = self.get_board()[row][col]
            self.get_board()[row][col] = temp
            self.empty = row, col - 1
            return True
        if (direction == "right"):
            if (col >= self.ncols - 1):
                return False
            temp = self.get_board()[row][col + 1]
            self.get_board()[row][col + 1] = self.get_board()[row][col]
            self.get_board()[row][col] = temp
            self.empty = row, col + 1
            return True
        return False

    def scramble(self, num_moves):
        seq = ["up", "down", "left", "right"]
        for i in range(num_moves):
            self.perform_move(random.choice(seq))

    def is_solved(self):
        return self.get_board() == create_tile_puzzle(self.nrows, self.ncols).get_board()

    def copy(self):
        return TilePuzzle([[i for i in j] for j in self.get_board()])

    def successors(self):
        seq = ["up", "down", "left", "right"]
        for s in seq:
            new_puzzle = self.copy()
            new_puzzle.perform_move(s)
            yield (s, new_puzzle)

    def iddfs_helper(self, limit, moves):
        if (self.is_solved()):
            yield moves
        if (limit > 0):
            for move, new_p in self.successors():
                temp = moves + [move]
                s = new_p.iddfs_helper(limit - 1, temp)
                for sol in s:
                    yield sol

    # Required
    def find_solutions_iddfs(self):
        limit = 0
        while True:
            result = False
            s = self.iddfs_helper(limit, [])
            for sol in s:
                yield sol
                result = True
            if (result):
                break
            limit += 1

    def heuristic(self):
        dist = 0
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.get_board()[row][col] == 0:
                    dist += abs(self.nrows - 1 - row)
                    dist += abs(self.ncols - 1 - col)
                else:
                    dist += abs((self.get_board()[row][col] - 1) // self.ncols - row)
                    dist += abs((self.get_board()[row][col] - 1) % self.ncols - col)
        return dist

    def a_star_helper(self, board):
        return tuple(tuple(i) for i in board)

    # Required
    def find_solution_a_star(self):
        frontier = PriorityQueue()
        frontier.put((self.heuristic(), [], self.copy(), 0))
        visited = set()
        while not frontier.empty():
            current = frontier.get()
            sol = current[1]
            p = current[2]
            if (p not in visited):
                if (p.is_solved()):
                    return sol
                for move, new_p in p.successors():
                    s = self.a_star_helper(new_p.get_board())
                    if (s not in visited):
                        temp = current[3]
                        frontier.put((new_p.heuristic() + temp, sol + [move], new_p, 1 + temp))
                visited.add(self.a_star_helper(p.get_board()))
        return None

############################################################
# Section 2: Grid Navigation
############################################################

def euclidean_dist(x1, y1, x2, y2):
    d1, d2 = x1 - x2, y1 - y2
    return math.sqrt(d1 * d1 + d2 * d2)

def succ_points(x1, y1, scene):
    for i in range(x1 - 1, x1 + 2):
        for j in range(y1 - 1, y1 + 2):
            if ((0 <= i < len(scene)) and (0 <= j < len(scene[0])) and (not scene[i][j])):
                yield (i, j)

def is_achieved(point, goal):
    return point == goal

def find_path(start, goal, scene):
    frontier = PriorityQueue()
    frontier.put((euclidean_dist(start[0], start[1], goal[0], goal[1]), [start], start, 0))
    visited = set()
    while not frontier.empty():
        current = frontier.get()
        sol = current[1]
        p = current[2]
        if (p not in visited):
            if (is_achieved(p, goal)):
                return sol
            for new_p in succ_points(p[0], p[1], scene):
                if (new_p not in visited):
                    temp = current[3] + euclidean_dist(p[0], p[1], new_p[0], new_p[1])
                    frontier.put((temp + euclidean_dist(new_p[0], new_p[1], goal[0], goal[1]), sol + [new_p], new_p, temp))
            visited.add(p)
    return None

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

class LinearDiskMovement(object):

    def __init__(self, length, n):
        self.length = length
        self.n = n

    def copy(self, n):
        return copy.deepcopy(n)

    def successors(self, row_new):
        for i in range(self.length):
            row = self.copy(row_new)
            if ((i >= 1) and (not row[i - 1])):
                temp = row[i - 1]
                row[i - 1] = row[i]
                row[i] = temp
                yield ((i, i - 1), row)
                row = self.copy(row_new)
            if ((i < self.length - 1) and (not row[i + 1])):
                temp = row[i + 1]
                row[i + 1] = row[i]
                row[i] = temp
                yield ((i, i + 1), row)
                row = self.copy(row_new)
            if ((i >= 1) and (row[i - 1]) and (i >= 2) and (not row[i - 2])):
                temp = row[i - 2]
                row[i - 2] = row[i]
                row[i] = temp
                yield ((i, i - 2), row)
                row = self.copy(row_new)
            if ((i < self.length - 1) and (row[i + 1]) and (i < self.length - 2) and (not row[i + 2])):
                temp = row[i + 2]
                row[i + 2] = row[i]
                row[i] = temp
                yield ((i, i + 2), row)
                row = self.copy(row_new)

    def find_helper(self, row):
        nrows = len(row)
        result = sum([(abs(nrows - i - x)) / 2 + abs((nrows - i - x)) % 2 for (i, x) in enumerate(row) if x > 0])
        return result

    def find_solution(self):
        frontier = PriorityQueue()
        temp = self.length - self.n
        node = [i + 1  if i < self.n else 0 for i in range(self.length)]
        frontier.put((self.find_helper(node), [], node))
        visited = set()
        goal = [self.length - i if i >= temp else 0 for i in range(self.length)]
        while not frontier.empty():
            current = frontier.get()
            s = current[1]
            p = current[2]
            visited.add(tuple(p))
            for move, new_p in self.successors(p):
                sol = s + [move]
                if (goal == new_p):
                    return sol
                if (tuple(new_p) not in visited):
                    temp = self.find_helper(new_p) + len(sol)
                    frontier.put((temp, sol, new_p))

def solve_distinct_disks(length, n):
    return LinearDiskMovement(length, n).find_solution()