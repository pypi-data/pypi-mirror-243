"""
Game views of the game
"""
import curses
from typing import Tuple

from time import sleep
from .patterns import Pattern
from .grid import LifeGrid

__all__ = ["CursesView"]


# pylint: disable=too-few-public-methods
class CursesView:
    """
    Displays the game of life using the curses standard library
    """

    def __init__(
        self,
        pattern: Pattern,
        gen: int = 10,
        frame_rate: int = 7,
        bbox: Tuple[int, int, int, int] = (0, 0, 20, 20),
    ):
        """
        Creates an instance of the curses view
        Args:
            pattern (Pattern): represents the life pattern to display on the screen
            gen (int): Number of generations the game will evolve through, the default is 10
            frame_rate (int): Frames per second, which is an indicator of the time between displaying one generation and
            another, the default is 7 frames per second
            bbox (tuple):  bounding box for the life grid. This is a tuple that represents which part of the life grid
            will be displayed. It should be a tuple of the form (start_col, start_row, end_col, end_row).
        """
        self.pattern = pattern
        self.gen = gen
        self.frame_rate = frame_rate
        self.bbox = bbox

    def show(self) -> None:
        """Displays the life grid on the screen"""
        curses.wrapper(self._draw)

    def _draw(self, screen: curses.window) -> None:
        """Displays consecutive generation of cells
        Args:
            screen: curses.window object that is passed in from the curses.wrapper function.
        """
        current_grid = LifeGrid(self.pattern)
        # sets the cursor's visibility, setting it to 0, means it is invisible
        curses.curs_set(0)
        screen.clear()

        # Checks if the current terminal window is large enough for the life grid to be display. This only needs to be
        # run once. A ValueError is raised if the terminal window is too small
        try:
            screen.addstr(0, 0, current_grid.as_string(self.bbox))
        except curses.error as exc:
            raise ValueError(
                f"Terminal too small for pattern {self.pattern.name}"
            ) from exc

        for _ in range(self.gen):
            current_grid.evolve()
            # On the current screen object, adds the given grid. The first two arguments define the row and column
            # where you want to start drawing the life grid. We start the drawing at (0, 0), which is the upper left
            # corner of the terminal window.
            screen.addstr(0, 0, current_grid.as_string(self.bbox))
            # refresh the screen to reflect the changes from the addstr() call
            screen.refresh()
            # sets the frame rate
            sleep(1 / self.frame_rate)
