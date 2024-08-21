from board.board import Board
from board.cell import Cell
from board.position import Position
from game.rules import is_in_bounds
from game.utils import Neighbors


def get_outflanked_discs(board: Board, row: int, col: int) -> list[Position]:
    current_player = board[row][col]
    opponents_discs: list[Position] = []

    for nrow, ncol in Neighbors(row, col):
        if not is_in_bounds(board, nrow, ncol):
            continue

        if board[nrow][ncol] == current_player:
            continue

        row_dir, col_dir = nrow - row, ncol - col
        opponents_discs_in_direction: list[Position] = []

        while is_in_bounds(board, nrow, ncol) and board[nrow][ncol] != Cell.EMPTY:
            if board[nrow][ncol] == current_player:
                opponents_discs.extend(opponents_discs_in_direction)
                break

            opponents_discs_in_direction.append(Position(nrow, ncol))

            nrow += row_dir
            ncol += col_dir

    return opponents_discs


def put_disc(board: Board, row: int, col: int, current_player: Cell) -> None:
    board[row][col] = current_player

    for nrow, ncol in get_outflanked_discs(board, row, col):
        board[nrow][ncol] = current_player
