from typing import Generator

from .cell import Cell
from .position import Position
from .utils import neighbors


class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.board = [[Cell.EMPTY] * width for _ in range(height)]
        self.board[height // 2 - 1][width // 2 - 1] = Cell.WHITE
        self.board[height // 2][width // 2] = Cell.WHITE
        self.board[height // 2 - 1][width // 2] = Cell.BLACK
        self.board[height // 2][width // 2 - 1] = Cell.BLACK

    def __getitem__(self, index: int) -> list[Cell]:
        return self.board[index]

    def __setitem__(self, index: int, value: list[Cell]) -> None:
        self.board[index] = value

    def __iter__(self) -> Generator[list[Cell], None, None]:
        for row in self.board:
            yield row

    def get_outflanked_discs(self, row: int, col: int) -> list[Position]:
        current_player = self[row][col]
        opponents_discs: list[Position] = []

        for nrow, ncol in neighbors(row, col):
            if not self.is_in_bounds(nrow, ncol):
                continue

            if self[nrow][ncol] == current_player:
                continue

            row_dir, col_dir = nrow - row, ncol - col
            opponents_discs_in_direction: list[Position] = []

            while self.is_in_bounds(nrow, ncol) and self[nrow][ncol] != Cell.EMPTY:
                if self[nrow][ncol] == current_player:
                    opponents_discs.extend(opponents_discs_in_direction)
                    break

                opponents_discs_in_direction.append(Position(nrow, ncol))

                nrow += row_dir
                ncol += col_dir

        return opponents_discs

    def put_disc(self, row: int, col: int, current_player: Cell) -> None:
        self[row][col] = current_player

        for nrow, ncol in self.get_outflanked_discs(row, col):
            self[nrow][ncol] = current_player

    def is_in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width
