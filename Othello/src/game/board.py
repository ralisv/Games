from typing import Generator

from .cell import Cell
from .position import Position
from .utils import get_opposing_player, neighbors


class Board:
    """
    Represents the game board of Othello.
    """

    history: list[tuple[Position, list[Position]]] = []
    """
    History of the game, where each element is a tuple of the position where the disc was put
    and the outflanked discs by result.
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
        self, position: Position, current_player: Cell
    ) -> Generator[Position, None, None]:
        """
        Get the discs that will be outflanked if a disc is placed at the given position.

        Args:
            position (Position): The position where the disc is to be placed.
            current_player (Cell): The current player's cell type.

        Returns:
            Generator[Position, None, None]: Generator of positions of the discs that will be outflanked.
        """
        for neighbor, direction in neighbors(position.row, position.col):
            if not self.is_in_bounds(neighbor):
                continue

            if self[neighbor.row][neighbor.col] == current_player:
                continue

            opponents_discs_in_direction: list[Position] = []

            current_pos = neighbor
            while (
                self.is_in_bounds(current_pos)
                and self[current_pos.row][current_pos.col] != Cell.EMPTY
            ):
                if self[current_pos.row][current_pos.col] == current_player:
                    yield from opponents_discs_in_direction
                    break

                opponents_discs_in_direction.append(current_pos)

                current_pos = Position(
                    current_pos.row + direction.row, current_pos.col + direction.col
                )

    def put_disc(self, position: Position, current_player: Cell) -> None:
        """
        Put a disc at the given position and outflank the opponent's discs (does not check if the move is valid).

        Args:
            position (Position): The position where the disc is to be placed.
            current_player (Cell): The player who is placing the disc.
        """
        new_discs = list(self.get_outflanked_discs(position, current_player))

        self[position.row][position.col] = current_player
        for outflanked_pos in new_discs:
            self[outflanked_pos.row][outflanked_pos.col] = current_player

        self.history.append((position, new_discs))

    def undo(self) -> None:
        """
        Undo the last move.
        """
        if not self.history:
            raise ValueError("No moves to undo")

        position, outflanked_discs = self.history.pop()
        opponent = get_opposing_player(self[position.row][position.col])
        self[position.row][position.col] = Cell.EMPTY

        for outflanked_pos in outflanked_discs:
            self[outflanked_pos.row][outflanked_pos.col] = opponent

    def is_in_bounds(self, position: Position) -> bool:
        """
        Check if the given position is within the bounds of the board.

        Args:
            position (Position): The position to check.

        Returns:
            bool: True if the position is within the bounds of the board, False otherwise.
        """
        return 0 <= position.row < self.height and 0 <= position.col < self.width
