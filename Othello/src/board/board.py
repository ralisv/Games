from typing import Generator

from .cell import Cell


class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.board = [[Cell.EMPTY] * width for _ in range(height)]

    def __getitem__(self, index: int) -> list[Cell]:
        return self.board[index]

    def __setitem__(self, index: int, value: list[Cell]) -> None:
        self.board[index] = value

    def __iter__(self) -> Generator[list[Cell], None, None]:
        for row in self.board:
            yield row
