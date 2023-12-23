import random

Position = tuple[int, int]


VICTORY = "VICTORY"
DEFEAT = "DEFEAT"
CONTINUE = "CONTINUE"


NUMBERS = {1: "１", 2: "２", 3: "３", 4: "４", 5: "５", 6: "６", 7: "７", 8: "８"}


class Field:
    def __init__(self) -> None:
        self.is_mine = False
        self.is_hidden = True
        self.is_flagged = False
        self.neighbours = 0

    def __str__(self, is_selected: bool = False) -> str:
        """
        Returns a string representation of the field.
        """
        if self.is_flagged:
            return "🏴"
        if self.is_hidden:
            return "⬛" if not is_selected else "🔳"
        if self.is_mine:
            return "💣"
        return NUMBERS[self.neighbours] if self.neighbours else "  "

    def __repr__(self) -> str:
        return self.__str__()


class Board:
    """
    Class managing the game board.
    """

    def __init__(self, height: int, width: int, mines: int):
        self.height = height
        self.width = width
        self.mines = mines
        self.to_reveal = height * width - mines + 1
        self.init_board()

    def init_board(self) -> None:
        """
        Initializes the board for the game.
        """
        self.board = self.create_board()
        self.assign_mines()
        self.assign_neighbours()

    def create_board(self) -> list[list[Field]]:
        """
        Creates a board of given height and width.
        """
        return [[Field() for _ in range(self.width)] for _ in range(self.height)]

    def assign_mines(self) -> None:
        """
        Assigns mines to the board randomly.
        """
        mine_positions = random.sample(
            sorted(
                i
                for i in range(self.height * self.width)
                if not self.is_in_corner(i // self.width, i % self.width)
            ),
            self.mines,
        )
        for i in mine_positions:
            self.board[i // self.width][i % self.width].is_mine = True

    def assign_neighbours(self) -> None:
        """
        Assigns the number of neighbouring mines to each field.
        """
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col].neighbours = self.count_neighbours(row, col)

    def count_neighbours(self, row: int, col: int) -> int:
        """
        Counts the number of neighbouring mines for a given field.
        """
        neighbours = 0
        for r in range(max(0, row - 1), min(self.height, row + 2)):
            for c in range(max(0, col - 1), min(self.width, col + 2)):
                if self.board[r][c].is_mine:
                    neighbours += 1
        return neighbours

    def get_field(self, row: int, col: int) -> Field:
        """
        Returns the field at the given position.
        """
        return self.board[row][col]

    def reveal_field(self, row: int, col: int) -> str:
        """
        Reveals the field at the given position.
        """
        # Validate coordinates
        if not (0 <= row < self.height) or not (0 <= col < self.width):
            raise Exception("Invalid coordinates")

        chosen_field = self.board[row][col]

        if chosen_field.is_flagged:
            chosen_field.is_flagged = False
            return CONTINUE

        chosen_field.is_hidden = False
        self.to_reveal -= 1

        if chosen_field.is_mine:
            return DEFEAT

        if chosen_field.neighbours == 0:
            self.flood_fill(row, col)

        if self.to_reveal == 0:
            for row in range(self.height):
                for col in range(self.width):
                    if self.board[row][col].is_mine:
                        self.board[row][col].is_flagged = True
                    else:
                        self.board[row][col].is_hidden = False

            return VICTORY

        return CONTINUE

    def flood_fill(self, row: int, col: int) -> None:
        """
        Reveals all neighbouring fields that are not mines.
        """
        if not self.board[row][col].is_hidden:
            self.board[row][col].is_hidden = False
            self.to_reveal -= 1

        stack = [(row, col)]

        while stack:
            row, col = stack.pop()

            if not self.board[row][col].neighbours == 0:
                continue

            for nrow, ncol in self.get_neighbors(row, col):
                if self.board[nrow][ncol].is_hidden:
                    self.board[nrow][ncol].is_hidden = False
                    self.to_reveal -= 1
                    stack.append((nrow, ncol))

    def flag_field(self, row: int, col: int) -> None:
        """
        Flags the field at the given position.
        """
        # Validate coordinates
        if not (0 <= row < self.height) or not (0 <= col < self.width):
            raise Exception("Invalid coordinates")

        chosen_field = self.board[row][col]

        if chosen_field.is_hidden:
            chosen_field.is_flagged = not chosen_field.is_flagged

    def get_neighbors(self, row: int, col: int) -> list[Position]:
        """
        Returns list of valid board coordinates.
        """
        neighbors: list[Position] = []
        for nrow in range(max(0, row - 1), min(self.height, row + 2)):
            for ncol in range(max(0, col - 1), min(self.width, col + 2)):
                if nrow == row and ncol == col:
                    continue

                neighbors.append((nrow, ncol))

        return neighbors

    def is_in_corner(self, row: int, col: int) -> bool:
        """
        Returns True if the field is in the corner.
        """
        return (row, col) in (
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        """
        return str(self.board)

    def print(self) -> None:
        """
        Prints the board.
        """
        print(*["".join(str(field) for field in row) for row in self.board], sep="\n")
