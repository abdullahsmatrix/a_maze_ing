from typing import Optional

from mazegen.cell import Cell
from mazegen.grid import Grid
from config.config import Config


class MazeWriter:
    """Writes Maze to a file in hexadecimal format."""

    def __init__(self, grid: Grid, config: Config,
                 path: Optional[str] = None) -> None:
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
            - Each cell is one hex digit encoding walls
            - Cells stored row by row, one row per line
            - Empty line
            - Entry coordinates
            - Exit coordinates
            - Solution path
        """
        try:
            with open(self.output_path, "w") as f:
                for y in range(self.grid.height):
                    row: str = ""
                    for x in range(self.grid.width):
                        cell = self.grid.get_cell(x, y)
                        hex_value = self.cell_to_hex(cell)
                        row += hex_value
                    f.write(row + "\n")

                f.write("\n")

                entry_str = f"{self.config.entry[0]},{self.config.entry[1]}"
                f.write(entry_str + "\n")

                exit_str = f"{self.config.exit[0]},{self.config.exit[1]}"
                f.write(exit_str + "\n")

                f.write(solution_path + "\n")

        except IOError as e:
            raise IOError(f"Failed to write output file: {e}")

    def cell_to_hex(self, cell: Cell) -> str:
        """Convert a cell's walls to hexadecimal.

        Args:
            cell: Cell to convert

        Returns:
            Hex digit (0-F) representing walls
            - Bit 0 (LSB): North
            - Bit 1: East
            - Bit 2: South
            - Bit 3: West
        """
        value = 0
        if cell.walls["N"]:
            value = value | (1 << 0)
        if cell.walls["E"]:
            value = value | (1 << 1)
        if cell.walls["S"]:
            value = value | (1 << 2)
        if cell.walls["W"]:
            value = value | (1 << 3)

        return format(value, "X")
