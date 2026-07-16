"""Maze walker kata: shortest orthogonal route through a string-art maze.

Kata catalogued at tddbuddy.com/katas/maze-walker; implementation and tests original (MIT),
machine-authored from the specification, 2026.
"""

from maze_walker.maze_walker import Maze, MazeWalker, NoPathError, walk_maze

__all__ = ["Maze", "MazeWalker", "NoPathError", "walk_maze"]
