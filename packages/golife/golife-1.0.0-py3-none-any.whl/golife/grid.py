"""
Life grid is used to evolve the generation to the next and represents this generation in a grid
"""
from typing import Tuple, DefaultDict
from collections import defaultdict
from .patterns import Pattern

# Characters used to represent living and dead cells
ALIVE = "♥"
DEAD = "."


class LifeGrid:
    """
    This takes care of 2 specific tasks:
    1. Evolving the grid to the next generation
    2. Providing a string representation of the grid

    """

    def __init__(self, pattern: Pattern):
        """Initializes a life grid and takes a pattern instance"""
        self.pattern = pattern

    def evolve(self) -> None:
        """Checks the currently alive cells and their neighbours to determine the next generation of alive cells"""

        # Define the delta coordinates for the neighbours of the target cell
        neighbours = (
            (-1, -1),  # above left
            (-1, 0),  # Above
            (-1, 1),  # above right
            (0, -1),  # left
            (0, 1),  # right
            (1, -1),  # below left
            (1, 0),  # below
            (1, 1),  # below right
        )

        # creates a dictionary for counting the number of living neighbours
        num_neighbours: DefaultDict[Tuple[int, int], int] = defaultdict(int)

        # Loop over the currently alive cells allowing a check for the neighbours of each living cell for the next
        # generation of living cells
        for row, col in self.pattern.alive_cells:
            # starts a loop over the neighbour deltas. This counts how many cells the current cell neighbours.
            # This count allows knowing the number of living neighbours for both living and dead cells
            for drow, dcol in neighbours:
                num_neighbours[(row + drow, col + dcol)] += 1

        # build a set containing the cells that will stay alive. First, we create a set of neighbours that have 2 or 3
        # alive neighbours themselves. Then, you find the cells that are common to both this and the living cells.
        stay_alive = {
            cell for cell, num in num_neighbours.items() if num in {2, 3}
        } & self.pattern.alive_cells

        # Create a set with the cells that will come alive. In this case, we create a set of neighbours that have
        # exactly 3 living neighbours. Then, we determine the cells that come alive by removing cells that are already
        # alive cells.
        come_alive = {
            cell for cell, num in num_neighbours.items() if num == 3
        } - self.pattern.alive_cells

        # updates the living cells with the set that results as the union of cells that stay alive and that come alive.
        self.pattern.alive_cells = stay_alive | come_alive

    def as_string(self, bbox: Tuple[int, int, int, int]) -> str:
        """Provides a way to represent the grid as a string that can be displayed in a terminal window.
        Args:
            bbox: Bounding box for the life grid. This box defines which part of the grid to display in the terminal
            window.
        """
        start_col, start_row, end_col, end_row = bbox
        display = [self.pattern.name.center(2 * (end_col - start_col))]
        for row in range(start_row, end_row):
            display_row = [
                ALIVE if (row, col) in self.pattern.alive_cells else DEAD
                for col in range(start_col, end_col)
            ]
            display.append(" ".join(display_row))

        return "\n".join(display)

    def __str__(self) -> str:
        """Returns a representation of the life grid as a string"""
        return (
            f"{self.pattern.name}: \n Alive Cells -> {sorted(self.pattern.alive_cells)}"
        )
