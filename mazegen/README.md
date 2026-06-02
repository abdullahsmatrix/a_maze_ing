# mazegen - Maze Generation and Solving Library

A reusable Python library for generating perfect mazes and solving them using classic algorithms.

## Features

- **Maze Generation**: Uses depth-first search with backtracking to generate perfect mazes
- **Maze Solving**: Uses breadth-first search to find the shortest path through a maze
- **Customizable Parameters**: Control maze size, seed for reproducibility, entry/exit points
- **Structured Data Access**: Access the maze as a grid of cells with individual wall information

## Installation

```bash
pip install mazegen
```

## Quick Start

### Basic Example

```python
from mazegen import Grid, MazeGenerator, MazeSolver

# Create a 21x21 grid
grid = Grid(width=21, height=21)

# Generate the maze with a specific seed for reproducibility
generator = MazeGenerator(grid, seed=42)
generator.generate()

# Solve the maze from (0, 0) to (20, 20)
solver = MazeSolver(grid, entry=(0, 0), exit_pos=(20, 20))
solution = solver.solve()

print(f"Solution path: {solution}")  # Returns string of moves: N, E, S, W
```

## Usage

### Creating a Grid

```python
from mazegen import Grid

# Create a grid of specified dimensions
grid = Grid(width=51, height=51)
```

### Generating a Maze

```python
from mazegen import MazeGenerator

# Create a generator
generator = MazeGenerator(grid)

# Generate without seed (random each time)
generator.generate()

# Or generate with a seed for reproducibility
generator = MazeGenerator(grid, seed=12345)
generator.generate()
```

### Solving a Maze

```python
from mazegen import MazeSolver

# Create a solver with entry and exit coordinates
solver = MazeSolver(grid, entry=(0, 0), exit_pos=(50, 50))

# Find the solution path
solution_path = solver.solve()

if solution_path:
    print(f"Path found: {solution_path}")  # e.g., "EEESSSEEENNN..."
else:
    print("No path exists")

# Check if maze is solvable
is_solvable = solver.is_solvable()
```

### Accessing the Maze Structure

```python
# Access individual cells
cell = grid.get_cell(x=10, y=10)

# Check if walls exist in a direction
# Walls are stored as a dictionary: {'N': bool, 'E': bool, 'S': bool, 'W': bool}
has_north_wall = cell.walls['N']
has_east_wall = cell.walls['E']

# Get neighboring cells
neighbors = grid.get_neighbors(cell)
```

## API Reference

### Grid

```python
class Grid:
    def __init__(self, width: int, height: int)
    def get_cell(self, x: int, y: int) -> Cell
    def get_neighbors(self, cell: Cell) -> Dict[str, Cell]
    def remove_wall(self, current: Cell, neighbor: Cell, direction: str)
```

### Cell

```python
class Cell:
    x: int                                  # X coordinate
    y: int                                  # Y coordinate
    walls: dict[str, bool]                 # {'N': bool, 'E': bool, 'S': bool, 'W': bool}
    visited: bool                          # Used by generation algorithm
    blocked: bool                          # Cells marked as blocked (obstacles)
```

### MazeGenerator

```python
class MazeGenerator:
    def __init__(self, grid: Grid, seed: Optional[int] = None)
    def generate() -> None  # Generates the maze
```

**Algorithm**: Uses depth-first search with backtracking to create perfect mazes (mazes with exactly one path between any two points).

### MazeSolver

```python
class MazeSolver:
    def __init__(self, grid: Grid, entry: tuple[int, int], exit_pos: tuple[int, int])
    def solve() -> Optional[str]           # Returns path as string or None
    def is_solvable() -> bool              # Returns whether maze has solution
```

**Algorithm**: Uses breadth-first search to find the shortest path.

**Return Format**: Solution paths are returned as a string of directions:
- `N`: Move North (up)
- `S`: Move South (down)
- `E`: Move East (right)
- `W`: Move West (left)

Example: `"EEESSEEESWWNNNNEE"` represents a sequence of moves to traverse the maze.

## Custom Parameters

### Maze Size

Adjust grid dimensions when creating a Grid:

```python
# Small maze
grid = Grid(width=11, height=11)

# Large maze
grid = Grid(width=101, height=101)
```

### Seed for Reproducibility

Use the seed parameter to generate identical mazes:

```python
# Generate the same maze every time
generator1 = MazeGenerator(grid, seed=42)
generator1.generate()

generator2 = MazeGenerator(grid, seed=42)
generator2.generate()
# Both will generate identical mazes
```

### Custom Entry/Exit Points

Specify any points in the grid as entry and exit:

```python
solver = MazeSolver(grid, entry=(5, 5), exit_pos=(45, 45))
solution = solver.solve()
```

## Advanced Usage

### Accessing Maze Data Structure

After generation, the maze is represented as a 2D grid of cells:

```python
# Access all cells
for row in grid.cells:
    for cell in row:
        print(f"Cell ({cell.x}, {cell.y}): walls={cell.walls}")

# Check if a path exists between two adjacent cells
current_cell = grid.get_cell(10, 10)
north_neighbor = grid.get_neighbors(current_cell)['N']

# If north wall is False, there's a path north
if not current_cell.walls['N']:
    print("Can move north")
```

### Special Features

The maze includes a decorative "42 pattern" (blocked cells) in the center of generated mazes.

## Version

Current version: 1.0.0

## License

See LICENSE file for details.

## Contributing

For issues or contributions, please contact the maintainers.
