from typing import Generator

from .cell import Cell
from .position import Position
from .utils import neighbors


class Board:
    """
    Represents the game board of Othello.
    """

    def __init__(self, height: int, width: int) -> None:
        """
        Initialize the game board with the four starting discs in the middle.

        Args:
            height (int): Height of the board.
            width (int): Width of the board.
        """
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

    def get_outflanked_discs(
        self, row: int, col: int, current_player: Cell
    ) -> Generator[Position, None, None]:
        """
        Get the discs that will be outflanked if a disc is placed at the given position.

        Args:
            row (int): Row index of the position.
            col (int): Column index of the position.

        Returns:
            list[Position]: List of positions of the discs that will be outflanked.
        """
        current_player = self[row][col]

        for nrow, ncol in neighbors(row, col):
            if not self.is_in_bounds(nrow, ncol):
                continue

            if self[nrow][ncol] == current_player:
                continue

            row_dir, col_dir = nrow - row, ncol - col
            opponents_discs_in_direction: list[Position] = []

            while self.is_in_bounds(nrow, ncol) and self[nrow][ncol] != Cell.EMPTY:
                if self[nrow][ncol] == current_player:
                    yield from opponents_discs_in_direction
                    break

                opponents_discs_in_direction.append(Position(nrow, ncol))

                nrow += row_dir
                ncol += col_dir

    def put_disc(self, row: int, col: int, current_player: Cell) -> None:
        """
        Put a disc at the given position and outflank the opponent's discs (does not check if the move is valid).

        Args:
            row (int): Row index of the position.
            col (int): Column index of the position.
            current_player (Cell): The player who is placing the disc.
        """
        self[row][col] = current_player

        for nrow, ncol in self.get_outflanked_discs(row, col, current_player):
            self[nrow][ncol] = current_player

    def is_in_bounds(self, row: int, col: int) -> bool:
        """
        Check if the given position is within the bounds of the board.

        Args:
            row (int): Row index of the position.
            col (int): Column index of the position.

        Returns:
            bool: True if the position is within the bounds of the board, False otherwise.
        """
        return 0 <= row < self.height and 0 <= col < self.width
