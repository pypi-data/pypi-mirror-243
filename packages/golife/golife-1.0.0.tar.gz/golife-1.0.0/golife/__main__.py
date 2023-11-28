"""
Entry point of the game
"""
import argparse
import sys

from golife import patterns, views
from golife.cli import get_command_line_args


def main() -> None:
    """Entry point of the game. Gets the command line arguments and shows either all patterns of the game or a single
    pattern based on the user input from the command line"""
    args = get_command_line_args()
    view = getattr(views, args.view)

    if args.all:
        for pattern in patterns.get_all_patterns():
            _show_pattern(view, pattern, args)
    else:
        _show_pattern(view, patterns.get_pattern(name=args.pattern), args)


def _show_pattern(
    view: views.CursesView,
    pattern: patterns.Pattern,
    args: argparse.Namespace,
) -> None:
    """Shows the pattern given the view, pattern and arguments from the command line"""
    try:
        v = view(pattern=pattern, gen=args.gen, frame_rate=args.fps)  # type: ignore[operator]
        v.show()
    # pylint: disable=broad-exception-caught
    except Exception as error:
        print(error, file=sys.stderr)


if __name__ == "__main__":
    main()
