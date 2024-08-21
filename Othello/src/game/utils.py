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


class Neighbors:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    from typing import Generator

    def __iter__(self) -> Generator[tuple[int, int], None, None]:
        for row_dir, col_dir in DIRECTIONS:
            yield self.row + row_dir, self.col + col_dir
