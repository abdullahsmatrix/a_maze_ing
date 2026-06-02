from mazegen.cell import Cell


class Grid:
    """Represents a grid of cells for maze generation."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize a grid."""
        self.width = width
        self.height = height
        self.cells: list = []

        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.cells.append(row)

    def get_cell(self, x: int, y: int) -> Cell:
        """Get a cell at coordinates."""
        return self.cells[y][x]

    def get_neighbors(self, cell: Cell) -> dict:
        """Get neighboring cells."""
        neighbors: dict = {}

        directions: dict = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors[direction] = self.get_cell(nx, ny)
        return neighbors

    def remove_wall(self, current: Cell, neighbor: Cell,
                    direction: str) -> None:
        """Remove wall between two cells."""
        opposite: dict[str, str] = {
            "N": "S",
            "E": "W",
            "S": "N",
            "W": "E"
        }
        if direction not in opposite:
            raise ValueError(f"Invalid Direction {direction}")
        current.walls[direction] = False
        neighbor.walls[opposite[direction]] = False
