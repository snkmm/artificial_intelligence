############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from typing import List, Tuple, Set, Optional

import numpy as np
from spherov2 import scanner
from spherov2.sphero_edu import SpheroEduAPI

from queue import PriorityQueue
import itertools

Vertex = Tuple[int, int]
Edge = Tuple[Vertex, Vertex]

############################################################
# Compare Different Searching Algorithms
############################################################

class Graph:
    """A directed Graph representation"""

    def __init__(self, vertices: Set[Vertex], edges: Set[Edge]):
        self.vertices = vertices
        self.edges = edges
        self.adj = {}
        for v in self.vertices:
            self.adj[v] = []
        for u, v in self.edges:
            self.adj[u] += [v]
            self.adj[v] += [u]

    def neighbors(self, u: Vertex) -> Set[Vertex]:
        """Return the neighbors of the given vertex u as a set"""
        return set(self.adj[u])

    def is_achived(self, point, goal):
        return point == goal

    def bfs(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use BFS algorithm to find the path from start to goal in the given graph.

        :return: a tuple (shortest_path, node_visited),
                 where shortest_path is a list of vertices that represents the path from start to goal, and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""
        frontier = [start]
        shortest_path, node_visited = ([], set())
        path = {start: None}
        while frontier:
            current = frontier.pop(0)
            if (self.is_achived(current, goal)):
                break
            for new_p in self.neighbors(current):
                if (new_p not in node_visited):
                    path[new_p] = current
                    frontier.append(new_p)
            node_visited.add(current)
        while goal:
            shortest_path.insert(0, goal)
            goal = path[goal]
        return shortest_path, node_visited

    def dfs(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use BFS algorithm to find the path from start to goal in the given graph.

        :return: a tuple (shortest_path, node_visited),
                 where shortest_path is a list of vertices that represents the path from start to goal, and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""
        frontier = [start]
        shortest_path, node_visited = ([], set())
        path = {start: None}
        while frontier:
            current = frontier.pop()
            if (self.is_achived(current, goal)):
                break
            for new_p in self.neighbors(current):
                if (new_p not in node_visited):
                    path[new_p] = current
                    frontier.append(new_p)
            node_visited.add(current)
        while goal:
            shortest_path.insert(0, goal)
            goal = path[goal]
        return shortest_path, node_visited

    def heuristic(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star(self, start: Vertex, goal: Vertex) -> Tuple[Optional[List[Vertex]], Set[Vertex]]:
        """Use A* algorithm to find the path from start to goal in the given graph.

        :return: a tuple (shortest_path, node_visited),
                 where shortest_path is a list of vertices that represents the path from start to goal, and None if
                 such a path does not exist; node_visited is a set of vertices that are visited during the search."""
        frontier = PriorityQueue()
        frontier.put((0, start, self.heuristic(start[0], start[1], goal[0], goal[1])))
        shortest_path, node_visited = ([], set())
        path = {start: None}
        n = {start: 0}
        while not frontier.empty():
            current = frontier.get()
            p = current[1]
            if (self.is_achived(p, goal)):
                break
            for new_p in self.neighbors(p):
                if (new_p not in node_visited):
                    s = new_p
                    if (s not in n):
                        path[s] = p
                        n[s] = n[p] + 1
                        frontier.put((n[s], s, n[s] + self.heuristic(s[0], s[1], goal[0], goal[1])))
            node_visited.add(p)
        while goal:
            shortest_path.insert(0, goal)
            goal = path[goal]
        return shortest_path, node_visited

    def tsp(self, start: Vertex, goals: Set[Vertex]) -> Tuple[Optional[List[Vertex]], Optional[List[Vertex]]]:
        """Use A* algorithm to find the path that begins at start and passes through all the goals in the given graph,
        in an order such that the path is the shortest.

        :return: a tuple (optimal_order, shortest_path),
                 where shortest_path is a list of vertices that represents the path from start that goes through all the
                 goals such that the path is the shortest; optimal_order is an ordering of goals that you visited in
                 order that results in the above shortest_path. Return (None, None) if no such path exists."""
        optimal_order, shortest_path = (None, None)
        for p in itertools.permutations(goals):
            order, path = tuple([start] + list(p)), []
            for o in range(len(order)):
                if (order[o] == order[-1]):
                    path.append(order[o])
                    continue
                temp = self.a_star(order[o], order[(o + 1) % len(order)])
                path += temp[0][0:-1]
            if (shortest_path is None):
                optimal_order, shortest_path = (order, path)
            else:
                if (len(shortest_path) > len(path)):
                    optimal_order, shortest_path = (order, path)
        return optimal_order, shortest_path
