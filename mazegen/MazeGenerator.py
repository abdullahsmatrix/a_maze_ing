import random
from typing import Optional

from mazegen.grid import Grid
from mazegen.cell import Cell


class MazeGenerator:
    """Generates a Maze using depth-first search algorithm."""

    def __init__(self, grid: Grid, seed: Optional[int] = None) -> None:
        """Initialize the maze generator.

        Takes grid to generate maze. Seed for reproducibility.
        """
        self.grid = grid
        if seed is not None:
            random.seed(seed)

    def generate(self) -> None:
        """Generate the maze."""
        self.mark_42()
        start = self.grid.get_cell(0, 0)
        self.dfs(start)

    def dfs(self, current: Cell) -> None:
        """Depth First Search to carve passage."""
        current.visited = True
        neighbors: dict[str, Cell] = self.grid.get_neighbors(current)
        directions: list[str] = list(neighbors.keys())
        random.shuffle(directions)

        for direction in directions:
            neighbor = neighbors[direction]
            if not neighbor.visited and not neighbor.blocked:
                self.grid.remove_wall(current, neighbor, direction)
                self.dfs(neighbor)

    def mark_42(self) -> None:
        """Mark 42 pattern in the maze with blocked cells."""
        pattern: list[list] = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pattern_height: int = len(pattern)
        pattern_width: int = len(pattern[0])

        # Center the pattern in the grid
        offset_x: int = (self.grid.width - pattern_width) // 2
        offset_y: int = (self.grid.height - pattern_height) // 2

        for y in range(pattern_height):
            for x in range(pattern_width):
                if pattern[y][x] == 1:
                    grid_x: int = offset_x + x
                    grid_y: int = offset_y + y
                    cell: Cell = self.grid.get_cell(grid_x, grid_y)
                    cell.blocked = True
