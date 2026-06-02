"""Interactive maze display with user controls."""

from typing import Dict, Tuple

from mazegen.grid import Grid
from mazegen.cell import Cell
from mazegen.MazeSolver import MazeSolver
from config.config import Config


class ColorScheme:
    """ANSI color codes for terminal rendering."""

    # Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

    # Styles
    BOLD = "\033[1m"
    DIM = "\033[2m"

    AVAILABLE_COLORS = {
        "1": ("RED", RED),
        "2": ("GREEN", GREEN),
        "3": ("YELLOW", YELLOW),
        "4": ("BLUE", BLUE),
        "5": ("MAGENTA", MAGENTA),
        "6": ("CYAN", CYAN),
        "7": ("WHITE", WHITE),
    }

    def __init__(self) -> None:
        """Initialize default colors."""
        self.wall_color = self.BOLD + self.CYAN
        self.path_color = self.YELLOW
        self.pattern_color = self.MAGENTA
        self.entry_color = self.GREEN
        self.exit_color = self.RED

    def display_palette(self) -> None:
        """Display available colors."""
        print("\n" + "=" * 50)
        print(self.BOLD + "AVAILABLE COLORS" + self.RESET)
        print("=" * 50)

        for key, (name, code) in self.AVAILABLE_COLORS.items():
            print(f"  {key}: {code}{self.BOLD}{name}{self.RESET}")

        print("=" * 50)

    def set_color(self, attribute: str, choice: str) -> bool:
        """Set a color attribute dynamically."""
        if choice not in self.AVAILABLE_COLORS:
            return False

        setattr(self, attribute, self.AVAILABLE_COLORS[choice][1])
        return True


class InteractiveRenderer:
    """Interactive maze renderer."""

    DIRECTION_MAP = {
        "N": (0, -1, "•"),
        "S": (0, 1, "•"),
        "E": (1, 0, "•"),
        "W": (-1, 0, "•"),
    }

    def __init__(self, grid: Grid, config: Config, solver: MazeSolver) -> None:
        """Initialize renderer."""
        self.grid = grid
        self.config = config
        self.solver = solver

        self.colors = ColorScheme()

        self.show_path = False
        self.solution_path = self.solver.solve() or ""

    # ==========================================================
    # SCREEN / DISPLAY
    # ==========================================================

    def clear_screen(self) -> None:
        """Clear terminal screen."""
        print("\033[H\033[J", end="")

    def display(self) -> None:
        """Display maze and status."""
        self.clear_screen()

        print(
            self.colors.BOLD
            + "A-MAZE-ING MAZE VIEWER"
            + self.colors.RESET
        )

        if self.show_path:
            print(
                f"Status: Path visible | "
                f"Path length: {len(self.solution_path)}"
            )
        else:
            print("Status: Path hidden")

        print()

        self.render()

    # ==========================================================
    # PATH PROCESSING
    # ==========================================================

    def build_visited_coordinates(self) -> Dict[Tuple[int, int], str]:
        """Convert solution path into coordinate -> arrow map."""
        visited: dict[tuple[int, int], str] = {}

        if not self.show_path or not self.solution_path:
            return visited

        x, y = self.config.entry
        visited[(x, y)] = "•"

        for direction in self.solution_path:
            if direction not in self.DIRECTION_MAP:
                continue

            dx, dy, arrow = self.DIRECTION_MAP[direction]

            x += dx
            y += dy

            if 0 <= x < self.grid.width and 0 <= y < self.grid.height:
                visited[(x, y)] = arrow

        return visited

    # ==========================================================
    # RENDERING
    # ==========================================================

    def render(self) -> None:
        """Render maze."""
        visited_coords = self.build_visited_coordinates()

        self.render_top_border()

        for y in range(self.grid.height):
            self.render_middle_row(y, visited_coords)
            self.render_bottom_row(y)

    def render_top_border(self) -> None:
        """Render top maze border."""
        line = self.colors.wall_color + "+"

        for _ in range(self.grid.width):
            line += "---+"

        line += self.colors.RESET

        print(line)

    def render_middle_row(self, y: int,
                          visited_coords:
                          Dict[Tuple[int, int], str]) -> None:
        """Render cell content row."""
        parts = [self.colors.wall_color + "|" + self.colors.RESET]

        for x in range(self.grid.width):
            cell = self.grid.get_cell(x, y)

            content, color = self.get_cell_display(
                x,
                y,
                cell,
                visited_coords,
            )

            parts.append(color + content + self.colors.RESET)

            if cell.walls["E"]:
                parts.append(
                    self.colors.wall_color
                    + "|"
                    + self.colors.RESET
                )
            else:
                parts.append(" ")

        print("".join(parts))

    def render_bottom_row(self, y: int) -> None:
        """Render bottom wall row."""
        parts = [self.colors.wall_color + "+"]

        for x in range(self.grid.width):
            cell = self.grid.get_cell(x, y)

            if cell.walls["S"]:
                parts.append("---+")
            else:
                parts.append("   +")

        parts.append(self.colors.RESET)

        print("".join(parts))

    # ==========================================================
    # CELL DISPLAY
    # ==========================================================

    def get_cell_display(self, x: int, y: int, cell: "Cell",
                         visited_coords:
                         Dict[Tuple[int, int], str]) -> Tuple[str,
                                                              str]:
        """Return cell content and color."""
        if (x, y) == self.config.entry:
            return " ◉ ", self.colors.entry_color

        if (x, y) == self.config.exit:
            return " ◆ ", self.colors.exit_color

        if cell.blocked:
            return " ▓ ", self.colors.pattern_color

        if (x, y) in visited_coords:
            arrow = visited_coords[(x, y)]
            return f" {arrow} ", self.colors.path_color

        return "   ", self.colors.RESET

    # ==========================================================
    # MENU
    # ==========================================================

    def show_menu(self) -> str:
        """Display menu and return user choice."""
        print("\n" + "=" * 50)
        print(self.colors.BOLD + "MAZE CONTROLS" + self.colors.RESET)
        print("=" * 50)

        print("1: Regenerate new maze")
        print("2: Show/Hide solution path")
        print("3: Change wall color")
        print("4: Change path color")
        print("5: Change 42 pattern color")
        print("6: View available colors")
        print("0: Exit")

        print("=" * 50)

        return input("Choose an option (0-6): ").strip()

    # ==========================================================
    # ACTIONS
    # ==========================================================

    def regenerate_maze(self) -> None:
        """Generate a new maze."""
        from mazegen.MazeGenerator import MazeGenerator

        new_grid = Grid(
            self.config.width,
            self.config.height,
        )

        generator = MazeGenerator(new_grid)
        generator.generate()

        self.grid = new_grid

        self.solver = MazeSolver(
            new_grid,
            self.config.entry,
            self.config.exit,
        )

        self.solution_path = self.solver.solve() or ""
        self.show_path = False

    def toggle_path(self) -> None:
        """Toggle solution path visibility."""
        self.show_path = not self.show_path

        status = "Showing" if self.show_path else "Hiding"

        print(f"\n✓ {status} solution path")

    def change_wall_color(self) -> None:
        """Change wall color."""
        self.change_color(
            "wall_color",
            "Choose wall color (1-7): ",
        )

    def change_path_color(self) -> None:
        """Change path color."""
        self.change_color(
            "path_color",
            "Choose path color (1-7): ",
        )

    def change_pattern_color(self) -> None:
        """Change pattern color."""
        self.change_color(
            "pattern_color",
            "Choose 42 pattern color (1-7): ",
        )

    def change_color(self, attribute: str, prompt: str) -> None:
        """Generic color changer."""
        self.colors.display_palette()

        choice = input(prompt).strip()

        if self.colors.set_color(attribute, choice):
            print("✓ Color changed!")
        else:
            print("✗ Invalid choice")

    # ==========================================================
    # MAIN LOOP
    # ==========================================================

    def interactive_loop(self) -> None:
        """Run interactive viewer."""
        actions = {
            "1": self.regenerate_maze,
            "2": self.toggle_path,
            "3": self.change_wall_color,
            "4": self.change_path_color,
            "5": self.change_pattern_color,
            "6": self.show_palette,
        }

        while True:
            self.display()

            choice = self.show_menu()

            if choice == "0":
                print(
                    "\n"
                    + self.colors.GREEN
                    + "Goodbye!"
                    + self.colors.RESET
                )
                break

            action = actions.get(choice)

            if action:
                action()
            else:
                print("\n✗ Invalid choice.")
                input("Press Enter to continue...")

    def show_palette(self) -> None:
        """Display color palette."""
        self.colors.display_palette()
        input("Press Enter to continue...")
