import sys
from pydantic import ValidationError

from MazeRenderer import InteractiveRenderer
from config.parser import parse_config, ConfigError
from mazegen.grid import Grid
from mazegen.MazeGenerator import MazeGenerator
from mazegen.MazeSolver import MazeSolver
from MazeWriter import MazeWriter
from MazeRenderer import InteractiveRenderer

def main():
    """Main entry point of the maze explorer. We check if config.txt is passed as arguement"""
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 a_maze_ing.py config.txt. Make sure config.txt included in Makefile.")
    
    config_path: str = sys.argv[1]

    try:
        config = parse_config(config_path)
        print(config)
    except (ConfigError, ValidationError) as err:
        if isinstance(err, ConfigError):
            print(err)
        elif isinstance(err, ValidationError):
            print(err.errors()[0]['msg'][12:])
        sys.exit(-1)
    
    try:
        #--- Create Grid using configurations ---#
        grid: Grid = Grid(config.width, config.height)
    
        #--- Generate Maze with seed as an optional arguement ---#
        generator: MazeGenerator = MazeGenerator(grid, seed=config.seed)
        generator.generate()

        #--- Solve Maze to get Path ---#
        solver: MazeSolver = MazeSolver(grid, config.entry, config.exit)
        solution_path: str = solver.solve() or ""

        #--- Write maze to output file ---#
        writer: MazeWriter = MazeWriter(grid, config)
        writer.write(solution_path)

        #--- Launching Interactive maze ---#
        renderer = InteractiveRenderer(grid, config, solver)
        renderer.interactive_loop()

    except Exception as e:
        print(f"Error during maze generation: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()