"""
Used for Patterns that will hold the name of a pattern and the co-ordinates of a live cells
"""
from typing import Set, Tuple, List, Dict
from dataclasses import dataclass
from pathlib import Path

# If using a Python version lower than 3.11, then the import will fail and try to import from the tomli library.
# Which will need to be installed
try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[no-redef]

PATTERNS_FILE = Path(__file__).parent / "patterns.toml"


@dataclass
class Pattern:
    """
    Holds the pattern information

    Args:
        name (str): Name of the pattern
        alive_cells (set):
        The set of tuples that will allow usage of set operations to determine the cells that will
        be alive in the next generation.
        Each tuple represents the coordinate of an alive cell in the life grid.
    """

    name: str
    alive_cells: Set[Tuple[int, int]]

    @classmethod
    def from_toml(cls, name: str, toml_data: Dict[str, List]) -> "Pattern":
        """Factory method to create an instance of Pattern provided a name and toml data with the grid for the living
        cells
        Args:
            name (str): name of the pattern
            toml_data: grid for the living cells
        Returns:
            Pattern: instance of pattern class
        """
        return cls(
            name=name, alive_cells={tuple(cell) for cell in toml_data["alive_cells"]}
        )


def get_pattern(name: str, filename: Path = PATTERNS_FILE) -> Pattern:
    """
    Retrieves a single pattern from the given file and creates a Pattern

    Args:
          name (str): name of the pattern to load from file.
          filename (Path): path to a pattern file to load
    Return:
        Pattern: instance of a pattern
    """
    data = tomllib.loads(filename.read_text(encoding="utf-8"))
    return Pattern.from_toml(name, toml_data=data[name])


def get_all_patterns(filename: Path = PATTERNS_FILE) -> List[Pattern]:
    """
    Retrieves all patterns from the given file and creates Patterns

    Args:
          filename (Path): path to a pattern file to load
    Return:
        List: list of pattern instances.
    """
    data = tomllib.loads(filename.read_text(encoding="utf-8"))
    return [
        Pattern.from_toml(name, toml_data=toml_data) for name, toml_data in data.items()
    ]
