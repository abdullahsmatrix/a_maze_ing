class Cell:
    def __init__(self, x: int, y: int) -> None:
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