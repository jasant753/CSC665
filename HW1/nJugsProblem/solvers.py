# ============================================================
# Solvers — Backtracking (two different implementations)
#           Placeholder for BFS, DFS
# Authors: S. El Alaoui and ChatGPT 5
# ============================================================

import math
from collections import deque
import time

from the3jugs import *

"""
Depth-first backtracking with simple 'explored' pruning.
Stores the best (lowest-cost) path of states encountered to any goal.
This is a recursive implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored 

"""


class BacktrackingSearch:
    def __init__(self, problem: SearchProblem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

        self.total_children = 0
        self.expanded_nodes = 0
        self.max_depth = 0
        self.shallow_depth = None

    def recurse(self, state, path, cost: int, depth: int):

        if depth > self.max_depth:
            self.max_depth = depth

        if self.problem.is_end(state):

            if cost < self.best_cost:
                self.best_cost = cost
                self.best_path = path[:]  # copy
                self.shallow_depth = depth
                # print(self.best_cost)
            return

        # Expand
        actions = list(self.problem.actions(state))

        self.expanded_nodes += 1
        self.total_children += len(actions)

        for action in actions:
            next_state = self.problem.succ(state, action)
            key = str(next_state)
            # key = next_state
            if key not in self.explored:
                self.explored.add(key)

                self.recurse(next_state, path + [next_state], cost + self.problem.cost(state, action), depth + 1)

    def solve(self):
        start = self.problem.start_state()
        self.explored.add(str(start))

        self.recurse(start, [], 0, 0)

        if self.expanded_nodes > 0:
            branching_factor = self.total_children / self.expanded_nodes
        else:
            branching_factor = 0

        return dict(
            best_cost=self.best_cost,
            best_path=[self.problem.start_state()] + (self.best_path or []),
            found=(self.best_path is not None),
            expanded=len(self.explored),
            b=branching_factor,
            D=self.max_depth,
            d=self.shallow_depth,
        )


"""
Depth-first backtracking with simple 'explored' pruning (iterative).
Stores the best (lowest-cost) path of states encountered to any goal.
This is an iterative implementation. 

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored

"""


class BacktrackingSearchIterative:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        start_key = str(start)
        self.explored.add(start_key)

        # Stack holds tuples: (state, path_from_after_start, cost_so_far)
        stack = [(start, [], 0, 0)]

        total_children = 0
        expanded_nodes = 0
        max_depth = 0
        shallow_depth = None

        while stack:
            state, path, cost, depth = stack.pop()

            if depth > max_depth:
                max_depth = depth

            # Goal check
            if self.problem.is_end(state):

                if cost < self.best_cost:
                    self.best_cost = cost
                    self.best_path = path[:]
                    shallow_depth = depth

                continue

            # Expand

            actions = list(self.problem.actions(state))

            expanded_nodes += 1
            total_children += len(actions)

            # To match recursive DFS order, push in reverse so first action is explored first.
            for action in reversed(actions):

                next_state = self.problem.succ(state, action)
                key = str(next_state)

                if key not in self.explored:

                    self.explored.add(key)

                    next_cost = cost + self.problem.cost(state, action)
                    next_depth = depth + 1

                    stack.append((next_state, path + [next_state], next_cost, next_depth))

        if expanded_nodes > 0:
            branching_factor = total_children / expanded_nodes
        else:
            branching_factor = 0

        return {
            "best_cost": self.best_cost,
            "best_path": [self.problem.start_state()] + (self.best_path or []),
            "found": (self.best_path is not None),
            "expanded": len(self.explored),
            "b": branching_factor,
            "D": max_depth,
            "d": shallow_depth
        }


"""
Add an iterative implementation of DFS.
BFS explores nodes level by leveland is guaranteed to find a goal at minimum depth (the fewest steps).

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""


class BFSSearch:
    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        start_key = str(start)
        self.explored.add(start_key)

        # Nodes at each level must be explored before moving to next level
        queue = deque([(start, [], 0, 0)])

        total_children = 0
        expanded_nodes = 0
        max_depth = 0

        while queue:
            state, path, cost, depth = queue.popleft()

            # Track max depth
            if depth > max_depth:
                max_depth = depth

            # Goal check
            # BFS returns at the first end state
            if self.problem.is_end(state):

                if expanded_nodes > 0:
                    branching_factor = total_children / expanded_nodes
                else:
                    branching_factor = 0

                return {
                    "best_cost": cost,
                    "best_path": path,
                    "found": True,
                    "expanded": len(self.explored),
                    "b": branching_factor,
                    "D": max_depth,
                    "d": depth
                }

            # Expand
            actions = list(self.problem.actions(state))
            expanded_nodes += 1
            total_children += len(actions)

            # No longer need reversed for queues
            for action in actions:
                next_state = self.problem.succ(state, action)
                key = str(next_state)

                if key not in self.explored:
                    self.explored.add(key)

                    next_cost = cost + self.problem.cost(state, action)
                    next_depth = depth + 1

                    queue.append((next_state, path + [next_state], next_cost, next_depth))


        if expanded_nodes > 0:
            branching_factor = total_children / expanded_nodes
        else:
            branching_factor = 0

        # If the loop finishes, BFS didn't find end state
        return {
            "best_cost": math.inf,
            "best_path": None,
            "found": False,
            "expanded": len(self.explored),
            "b": branching_factor,
            "D": max_depth,
            "d": None
        }


"""
Add an iterative implementation of DFS.
DFS explores along a path as deep as possible before backtracking 
and returns the first solution found, which may not be the shortest.

returns a dictionary with the following informatin: 
    best_cost= path cost (i.e. number of steps from start to the goal),
    best_path= [s_0, ..., s*],
    found= boolean : path found or not 
    expanded= # of state explored
"""


class DFSSearch:

    def __init__(self, problem):
        self.best_cost = math.inf
        self.best_path = None
        self.explored = set()
        self.problem = problem

    def solve(self):
        start = self.problem.start_state()
        start_key = str(start)
        self.explored.add(start_key)

        stack = [(start, [], 0, 0)]

        total_children = 0
        expanded_nodes = 0
        max_depth = 0

        while stack:
            state, path, cost, depth = stack.pop()

            # Track max depth
            if depth > max_depth:
                max_depth = depth

            # Goal check
            # Search ends as soon as we reach end state
            if self.problem.is_end(state):

                if expanded_nodes > 0:
                    branching_factor = total_children / expanded_nodes
                else:
                    branching_factor = 0

                return {
                    "best_cost": cost,
                    "best_path": path,
                    "found": True,
                    "expanded": len(self.explored),
                    "b": branching_factor,
                    "D": max_depth,
                    "d": depth
                }

            # Expand
            actions = list(self.problem.actions(state))

            expanded_nodes += 1
            total_children += len(actions)

            # Push in reverse so first action is explored first.
            for action in reversed(actions):
                next_state = self.problem.succ(state, action)
                key = str(next_state)

                if key not in self.explored:
                    self.explored.add(key)

                    next_cost = cost + self.problem.cost(state, action)
                    next_depth = depth + 1

                    stack.append((next_state, path + [next_state], next_cost, next_depth))

        if expanded_nodes > 0:
            branching_factor = total_children / expanded_nodes
        else:
            branching_factor = 0

        # If the loop finishes, DFS didn't find end state
        return {
            "best_cost": math.inf,
            "best_path": None,
            "found": False,
            "expanded": len(self.explored),
            "b": branching_factor,
            "D": max_depth,
            "d": None
        }


