from game.position import Position

from .board import Board
from .cell import Cell
from .utils import neighbors


def is_empty(board: Board, row: int, col: int) -> bool:
    """
    Check if a cell on the board is empty.

    Args:
        board (Board): The game board.
        row (int): The row index of the cell.
        col (int): The column index of the cell.

    Returns:
        bool: True if the cell is empty, False otherwise.
    """
    return board[row][col] == Cell.EMPTY


def outflanks_opponent(board: Board, row: int, col: int, current_player: Cell) -> bool:
    """
    Check if placing a disc at the given position outflanks any opponent's discs.

    Args:
        board (Board): The game board.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        current_player (Cell): The current player's cell type.

    Returns:
        bool: True if the move outflanks opponent's disc(s), False otherwise.

    Raises:
        ValueError: If the current player's cell is empty.
    """
    if current_player == Cell.EMPTY:
        raise ValueError("Current player cell cannot be empty")

    for _ in board.get_outflanked_discs(Position(row, col), current_player):
        return True

    return False


def is_adjacent_to_opponent(
    board: Board, row: int, col: int, current_player: Cell
) -> bool:
    """
    Check if the given position is adjacent to an opponent's disc.

    Args:
        board (Board): The game board.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        current_player (Cell): The current player's cell type.

    Returns:
        bool: True if the position is adjacent to an opponent's disc, False otherwise.

    Raises:
        ValueError: If the current player's cell is empty.
    """
    if Cell == Cell.EMPTY:
        raise ValueError("Current player cell cannot be empty")

    for (nrow, ncol), _ in neighbors(row, col):
        if not board.is_in_bounds(Position(nrow, ncol)):
            continue

        if board[nrow][ncol] != current_player:
            return True

    return False


def is_valid_move(board: Board, position: Position, current_player: Cell) -> bool:
    """
    Check if a move is valid according to Othello rules.

    Args:
        board (Board): The game board.
        row (int): The row index of the cell.
        col (int): The column index of the cell.
        current_player (Cell): The current player's cell type.

    Returns:
        bool: True if the move is valid, False otherwise.
    """
    row, col = position
    return (
        board.is_in_bounds(Position(row, col))
        and is_empty(board, row, col)
        and is_adjacent_to_opponent(board, row, col, current_player)
        and outflanks_opponent(board, row, col, current_player)
    )
