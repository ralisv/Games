from typing import Generator

from game.cell import Cell
from game.position import Position

DIRECTIONS = {
    (0, 1),  # right
    (1, 1),  # down-right
    (1, 0),  # down
    (1, -1),  # down-left
    (0, -1),  # left
    (-1, -1),  # up-left
    (-1, 0),  # up
    (-1, 1),  # up-right
}


def neighbors(row: int, col: int) -> Generator[tuple[Position, Position], None, None]:
    for row_dir, col_dir in DIRECTIONS:
        yield Position(row + row_dir, col + col_dir), Position(row_dir, col_dir)


def get_opposing_player(current_player: Cell) -> Cell:
    """
    Get the opposing player.

    Args:
        current_player (Cell): The current player.

    Returns:
        Cell: The opposing player.
    """
    return Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK
