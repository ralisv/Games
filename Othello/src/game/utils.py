from typing import Generator

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


def neighbors(row: int, col: int) -> Generator[tuple[int, int], None, None]:
    for row_dir, col_dir in DIRECTIONS:
        yield row + row_dir, col + col_dir
