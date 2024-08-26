from .board import Board
from .cell import Cell
from .rules import is_valid_move


def is_game_over(board: Board) -> bool:
    return not can_play(board, Cell.BLACK) and not can_play(board, Cell.WHITE)


def can_play(board: Board, current_player: Cell) -> bool:
    return any(
        is_valid_move(board, row, col, current_player)
        for row in range(board.height)
        for col in range(board.width)
    )


def get_scores(board: Board) -> dict[Cell, int]:
    return {
        Cell.BLACK: sum(row.count(Cell.BLACK) for row in board),
        Cell.WHITE: sum(row.count(Cell.WHITE) for row in board),
    }
