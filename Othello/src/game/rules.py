from board.board import Board
from board.cell import Cell
from game.utils import Neighbors


def is_in_bounds(board: Board, row: int, col: int) -> bool:
    return 0 <= row < board.height and 0 <= col < board.width


def is_empty(board: Board, row: int, col: int) -> bool:
    return board[row][col] == Cell.EMPTY


def outflanks_opponent(board: Board, row: int, col: int, current_player: Cell) -> bool:
    if Cell == Cell.EMPTY:
        raise ValueError("Current player cell cannot be empty")

    for nrow, ncol in Neighbors(row, col):
        if not is_in_bounds(board, nrow, ncol):
            continue

        if board[nrow][ncol] == current_player:
            continue

        row_dir, col_dir = nrow - row, ncol - col

        while is_in_bounds(board, nrow, ncol) and board[nrow][ncol] != Cell.EMPTY:
            if board[nrow][ncol] == current_player:
                return True

            nrow += row_dir
            ncol += col_dir

    return False


def is_adjacent_to_opponent(
    board: Board, row: int, col: int, current_player: Cell
) -> bool:
    if Cell == Cell.EMPTY:
        raise ValueError("Current player cell cannot be empty")

    for nrow, ncol in Neighbors(row, col):
        if not is_in_bounds(board, nrow, ncol):
            continue

        if board[nrow][ncol] != current_player:
            return True

    return False


def is_valid_move(board: Board, row: int, col: int, current_player: Cell) -> bool:
    return (
        is_in_bounds(board, row, col)
        and is_empty(board, row, col)
        and is_adjacent_to_opponent(board, row, col, current_player)
        and outflanks_opponent(board, row, col, current_player)
    )
