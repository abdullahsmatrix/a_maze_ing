*This project has been created as part of the 42 curriculum by amamun, pbishnoi.*

# a_maze_ing

## Description

A maze generation and solving library with interactive exploration. The project generates perfect mazes using randomized depth-first search, solves them via breadth-first search, and provides an interactive terminal-based visualization with customizable colors. All mazes include a centered 42 pattern as a distinctive feature.

## Instructions

### Installation

```bash
make install
```

Installs dependencies using Poetry (requires Python >=3.13).

### Execution

```bash
make run
```

Runs the interactive maze explorer using `config.txt`.

### Compilation & Linting

```bash
make lint          # Run flake8 and mypy type checking
make lint-strict   # Apply strict mypy rules
make clean         # Remove cache and temporary files
```

## Configuration File Structure

Config file format (key=value, case-insensitive):

```
WIDTH=20              # Grid width (integer)
HEIGHT=20             # Grid height (integer)
ENTRY=0,0             # Entry coordinates (x,y)
EXIT=19,19            # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # Output filename
PERFECT=True          # Generate perfect maze (boolean)
SEED=42               # Optional: reproducible generation
```

Config is validated using Pydantic. Entry and exit must be within bounds and different from each other.

## Maze Generation Algorithm: Randomized Depth-First Search

### Algorithm Choice

**Randomized Depth-First Search (DFS)** was selected for:
- **Efficiency**: O(width × height) complexity
- **Perfect mazes**: Guarantees exactly one solution path
- **Stack-based**: Natural implementation with recursion
- **Fast generation**: Suitable for real-time interactive use

### Implementation Details

1. **Initialization**: All cells start with walls on all sides
2. **42 Pattern**: Blocked cells are marked in a centered 42-shaped pattern
3. **DFS Traversal**: Starting from (0,0), recursively visit unvisited neighbors in random order
4. **Wall Removal**: Carve passages between current and neighbor cells
5. **Termination**: When no unvisited neighbors exist, backtrack

## Reusable Components

### `mazegen` Package

The `mazegen` library is independently reusable:

**Core Classes**:
- `Grid`: Cell management and neighbor queries
- `Cell`: Individual maze cells with wall state
- `MazeGenerator`: DFS-based maze generation with custom patterns
- `MazeSolver`: BFS pathfinding

For further information see package documentation.

## Team & Project Management

### Team Roles

| Member | Responsibility |
|--------|-----------------|
| **amamun** | Maze generation algorithm, DFS implementation, Grid/Cell structure |
| **pbishnoi** | Interactive renderer, ANSI color system, terminal UI, user controls |
| **Both** | Documentation, packaging, config and parsing, solver algorithm, writer |

### Project Evolution

**Initial Plan**:
- Spent time on architecting application and efficiently implementing algorithms.
- Initially we planned to generate a simple maze using DFS algorithm and A-Star pathfinding to solve maze.
- Roadmap: Config & Parse -> Generate Maze -> Solve Maze -> Write -> Interactive Rendering

**What Changed**:
- As we evolved, we decided to go with BFS since it is simpler for perfect maze. 
- Added interactive terminal rendering with real-time path display
- Integrated 42 pattern as requirement
- Type hints added for code quality

### What Worked Well

- Modular package design enabled parallel development
- Pydantic configuration reduced validation overhead
- Type hints caught early integration issues
- DFS naturally suited recursive problem

### What Could Improve

- BFS could cache solutions for repeated queries
- Interactive renderer could support mouse input
- Maze save/load format for analysis
- Additional generation algorithms as options

### Tools Used

- **Poetry**: Dependency management
- **Pydantic**: Configuration validation
- **Flake8**: Code style linting
- **mypy**: Static type checking (Python >=3.13)
- **Makefile**: Task automation

## Resources

### Data Structure
- [Queue Data Structure](https://www.geeksforgeeks.org/dsa/queue-data-structure/) - Queue data structure overview
- Grokking Algorithms: An Illustrated Guide for Programmers and Other Curious People
                                                                        -Aditya Y. Bhargava

### Maze Generation & Algorithm References
- [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) - Algorithm overview
- [Depth-First Search](https://www.geeksforgeeks.org/dsa/depth-first-search-or-dfs-for-a-graph/) - DFS Algorithm
- [Algorithms Visualization](https://visualgo.net/en) - Visualizing Algorithms for better understanding.
- [Breadth-First Search](https://www.geeksforgeeks.org/dsa/breadth-first-search-or-bfs-for-a-graph/) - BFS algorithm

### Python References
- [Pydantic Documentation](https://pydantic.dev/docs/validation/latest/concepts/models) - Pydantic concept and usage
- [Poetry Documentation](https://python-poetry.org/docs/) - Poetry Usage
- [Python Documentation](https://docs.python.org/3/tutorial/classes.html) OOP Methodologies recap

### AI Usage

**ChatGPT was used for**:
- Application design and architecture
- Python library recommendation and Control flow
- Algorithm Recommendation and research
