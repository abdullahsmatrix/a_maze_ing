class Cell:
    """Represents a single cell in a maze grid."""

    def __init__(self, x: int, y: int) -> None:
        """Initialize a cell."""
        self.x = x
        self.y = y
        self.walls: dict[str, bool] = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.visited: bool = False
        self.blocked: bool = False
