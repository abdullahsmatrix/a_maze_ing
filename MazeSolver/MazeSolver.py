from collections import deque
from typing import Optional
from maze.grid import Grid
from maze.cell import Cell


class MazeSolver:
    """Solving Maze by finding shortest path from entry to exit"""
    def __init__(self, grid: Grid, entry: tuple[int, int], exit_pos: tuple[int, int]) -> None:
        self.grid = grid
        self.entry = entry
        self.exit = exit_pos
    

    def solve(self) -> Optional[str]:
        """Find the shortest path from entry to exit.
        
        Returns:
            A string of moves (N, E, S, W) if path exists, None otherwise
        """
        path = self.bfs()
        return path
    

    def bfs(self) -> Optional[str]:
        """Breadth-First Search algorithm to find the shortest path.
        Returns path as a string of directions or None if path does not exists
        """

        queue = deque([(self.entry, "")])
        visited = {self.entry}
        directions_map: dict[str, tuple] = {
            "N": (0, -1),
            "S": (0, 1),
            "E": (1, 0),
            "W": (-1, 0)
        }

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == self.exit:
                return path
            
            cell = self.grid.get_cell(x, y)

            for direction, (dx, dy) in directions_map.items():
                # check if wall is open in this direction
                if cell.walls[direction]:
                    continue
                nx, ny = x + dx, y + dy

                #check bounds
                if not (0 <= nx < self.grid.width and 0 <= ny < self.grid.height):
                    continue

                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + direction))
        return None
    
    def is_solvable(self) -> bool:
        """ Check if maze has a solution.
        Returns: True if path exist from entry to exit.
        """
        return self.bsf() is not None

