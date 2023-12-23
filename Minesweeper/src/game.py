import argparse
import os
import sys
from email.policy import default

from blessed import Terminal

# Add the parent directory to the sys.path list
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from board import Board

term = Terminal()


def print_board(board: Board, row: int, col: int) -> None:
    with term.location():
        for r in range(board.height):
            for c in range(board.width):
                field = board.get_field(r, c)
                if r == row and c == col:
                    # Highlight the current field
                    if not field.is_hidden or field.is_flagged:
                        print(term.reverse(field.__str__(is_selected=True)), end="")
                    else:
                        print(field.__str__(is_selected=True), end="")
                else:
                    print(str(field), end="")
            print()


def main():
    parser = argparse.ArgumentParser(description="CLI Minesweeper Game")

    # Adding the command-line arguments
    parser.add_argument(
        "--height",
        type=int,
        default=None,
        help="Height of the game grid. Default is 10.",
    )
    parser.add_argument(
        "--width", type=int, default=None, help="Width of the game grid. Default is 10."
    )
    parser.add_argument(
        "--mines",
        type=int,
        default=None,
        help="Number of mines in the game grid. Default is 1/6 of the total number of fields.",
    )

    args = parser.parse_args()

    h, w = args.height or 10, args.width or 10
    m = args.mines or (h * w) // 6

    board = Board(h, w, m)

    with term.cbreak(), term.hidden_cursor():
        # The cbreak context manager allows you to get user inputs immediately without waiting for Enter
        # The hidden_cursor context manager hides the console cursor

        row, col = 0, 0
        while True:
            print(term.clear)  # Clear the console

            print_board(board, row, col)

            print(
                term.move_yx(board.height, 0)
            )  # Move the console cursor to below the board
            print(
                f"Use arrow keys to move, Space to reveal a field, and 'q' to quit, you still have {board.to_reveal} fields to reveal!"
            )

            key = term.inkey()  # Get a user key press

            if key.code == term.KEY_UP and row > 0:
                row -= 1
            elif key.code == term.KEY_DOWN and row < board.height - 1:
                row += 1
            elif key.code == term.KEY_LEFT and col > 0:
                col -= 1
            elif key.code == term.KEY_RIGHT and col < board.width - 1:
                col += 1
            elif key == " ":
                # Reveal the field
                status = board.reveal_field(row, col)

                match status:
                    case "CONTINUE":
                        pass

                    case "VICTORY":
                        print(term.clear)  # Clear the console
                        print_board(board, row, col)
                        print(term.move_yx(board.height + 1, 0) + "You won!")
                        break

                    case "DEFEAT":
                        print(term.clear)  # Clear the console
                        print_board(board, row, col)
                        print(
                            term.move_yx(board.height + 1, 0) + "You stepped on a mine!"
                        )
                        break

                    case _:
                        pass

            if key.lower() == "q":
                break

            if key.lower() == "f":
                board.flag_field(row, col)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
