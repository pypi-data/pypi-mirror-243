"""
Defines the CLI command arguments
"""
import argparse
from argparse import Namespace

from golife import views
from .patterns import get_all_patterns


def get_command_line_args() -> Namespace:
    """
    Creates a parser and adds arguments for the parser returning the namespace for the argument parser to use in a CLI
    """
    parser = argparse.ArgumentParser(
        prog="golife", description="Conway's Game Of Life in the terminal"
    )

    parser.add_argument(
        "-p",
        "--pattern",
        choices=[pat.name for pat in get_all_patterns()],
        default="Blinker",
        help="take a pattern for the game of life, default: %(default)s",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="show all available patterns in a sequence",
    )

    parser.add_argument(
        "-v",
        "--view",
        choices=views.__all__,
        default="CursesView",
        help="display the life grid in a specific view (default: %(default)s)",
    )

    parser.add_argument(
        "-g",
        "--gen",
        metavar="NUM_GENERATIONS",
        type=int,
        default=10,
        help="number of generations (default: %(default)s)",
    )

    parser.add_argument(
        "-f",
        "--fps",
        metavar="FRAMES_PER_SECOND",
        type=int,
        default=7,
        help="frames per second (default: %(default)s)",
    )

    return parser.parse_args()
