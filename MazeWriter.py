from typing import Optional
from maze.grid import Grid
from config.config import Config

class MazeWriter:
    """Writes Maze to a file in hexadecimal format."""

    def __init__(self, grid: Grid, config: Config, path: Optional[str] = None) -> None:
        """Initialize the writer.
        
        Args:
            grid: The maze grid
            config: Configuration containing entry, exit, and output file
            path: Optional override for output path
        """
        self.grid = grid
        self.config = config
        self.output_path = path or config.output_file

    def write(self, solution_path: str = "") -> None:
        """Write maze to file in hex format.
        
        Args:
            solution_path: Path from entry to exit as string of N/E/S/W
        
        Format:
            - Each cell is one hex digit encoding walls (bit 0=N, 1=E, 2=S, 3=W)
            - Cells stored row by row, one row per line
            - Empty line
            - Entry coordinates
            - Exit coordinates
            - Solution path
        """
        try:
            with open(self.output_path, "w") as f:
                """Write maze in hex format"""
                for y in range(self.grid.height):
                    row: str = ""
                    for x in range(self.grid.width):
                        cell = self.grid.get_cell(x,y)
                        hex_value = self.cell_to_hex(cell)
                        row += hex_value
                    f.write(row + "\n")
                
                # Empty line separator
                f.write("\n")

                # Entry coordinates
                f.write(f"") 