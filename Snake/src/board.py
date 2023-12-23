import random
from collections import deque

from constants import CELLS, EDGES, Position
from maps import Map


class Board:
    map: list[list[str]]
    rows: int
    cols: int
    snake: deque[Position]
    direction: tuple[int, int]

    def __init__(self, map: Map) -> None:
        self.map: list[list[str]] = [
            [CELLS.WALL if not c else CELLS.EMPTY for c in row] for row in map.map
        ]

        snake = map.snake

        if not self.map or not all(len(row) == len(self.map[0]) for row in self.map):
            raise ValueError("Invalid map")

        self.rows = len(self.map)
        self.cols = len(self.map[0])

        if not snake:
            raise ValueError("No snake")

        srow, scol = snake[0]
        if self.map[srow][scol] != CELLS.EMPTY:
            raise ValueError("Invalid starting snake position")

        self.map[srow][scol] = CELLS.HEAD

        for row, col in snake[1:]:
            if self.map[row][col] != CELLS.EMPTY:
                raise ValueError("Invalid starting snake position")

            self.map[row][col] = CELLS.SNAKE

        self.snake: deque[Position] = deque(snake)
        self.direction = map.starting_direction

        for _ in range(map.fruits):
            self.place_fruit()

    def __str__(self) -> str:
        """Returns a string representation of the board,
        utilized for the game's CLI

        Returns:
            str: The string representation of the board
        """
        board_with_borders: list[str] = []

        # Top border
        board_with_borders.append(
            EDGES.WALL_TOP_LEFT
            + EDGES.WALL_HORIZONTAL * (self.cols - 2)
            + EDGES.WALL_TOP_RIGHT
        )

        # Map rows with side borders
        for row in self.map:
            board_with_borders.append(
                EDGES.WALL_VERTICAL + "".join(row) + EDGES.WALL_VERTICAL
            )

        # Bottom border
        board_with_borders.append(
            EDGES.WALL_BOTTOM_LEFT
            + EDGES.WALL_HORIZONTAL * (self.cols - 2)
            + EDGES.WALL_BOTTOM_RIGHT
        )

        return "\n".join(board_with_borders)

    def place_fruit(self) -> None:
        """Places a fruit on the board

        Raises:
            ValueError: If there are no free spaces left
        """
        free_spaces = [
            (r, c)
            for r, row in enumerate(self.map)
            for c, cell in enumerate(row)
            if cell == CELLS.EMPTY
        ]
        if not free_spaces:
            raise ValueError("No free spaces left")

        row, col = random.choice(free_spaces)

        self.map[row][col] = CELLS.FRUIT

    def move_snake(self) -> bool:
        """Moves the snake one step in the current direction

        Returns:
            bool: Whether the snake is still alive
        """
        rowHead, colHead = self.snake[0]
        rowDelta, colDelta = self.direction
        newRowHead, newColHead = (rowHead + rowDelta) % self.rows, (
            colHead + colDelta
        ) % self.cols

        if self.map[newRowHead][newColHead] == CELLS.WALL:
            return False

        # If the snake tries to run into any part of itself except the tail, end the game
        elif (
            self.map[newRowHead][newColHead] == CELLS.SNAKE
            and (newRowHead, newColHead) != self.snake[-1]
        ):
            return False

        if self.map[newRowHead][newColHead] == CELLS.FRUIT:
            self.place_fruit()
        else:
            # Remove the tail of the snake (this also handles the case where the snake is moving into its tail)
            trow, tcol = self.snake.pop()
            self.map[trow][tcol] = CELLS.EMPTY

        self.map[newRowHead][newColHead] = CELLS.HEAD

        self.snake.appendleft((newRowHead, newColHead))

        if len(self.snake) > 1:
            srow, scol = self.snake[1]
            self.map[srow][scol] = CELLS.SNAKE

        return True

    def set_direction(self, direction: tuple[int, int]) -> None:
        self.direction = (
            direction
            if direction != tuple(-x for x in self.direction)
            else self.direction
        )
