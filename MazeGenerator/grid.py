from MazeGenerator.cell import Cell

class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.cells: list = []

        for y in range(height):
            row = []
            for x in range(width):
                row.append(Cell(x, y))
            self.cells.append(row)
    
    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]
    
    def get_neighbors(self, cell: Cell) -> Cell:
        nieghbors: dict = {}

        directions: dict = {
            "N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0)
        }

        for direction, (dx, dy) in directions.items():
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                nieghbors[direction] = self.get_cell(nx, ny)
        return nieghbors
    
    def remove_wall(self, current: Cell, neighbor: Cell, direction: str) -> None:
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

