from curses import wrapper

from board.cell import Cell
from cli.core import (
    handle_no_valid_moves,
    initialize_board,
    initialize_screen,
    move_cursor,
    print_board,
)
from game.core import put_disc
from game.rules import is_valid_move


def _main(stdscr):
    initialize_screen(stdscr)

    board = initialize_board()
    current_player: Cell = Cell.BLACK
    cursor_row, cursor_col = 0, 0

    print_board(stdscr, board, cursor_row, cursor_col, current_player)

    while True:
        key = stdscr.getch()
        if key == ord("q"):
            break

        new_row, new_col = move_cursor(
            stdscr, board, key, cursor_row, cursor_col, current_player
        )

        if key in [ord(" "), 10]:
            if is_valid_move(board, new_row, new_col, current_player):
                put_disc(board, new_row, new_col, current_player)
                current_player = (
                    Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK
                )
                print_board(stdscr, board, new_row, new_col, current_player)
            else:
                continue

        cursor_row, cursor_col = new_row, new_col

        if not any(
            is_valid_move(board, row, col, current_player)
            for row in range(board.height)
            for col in range(board.width)
        ):
            current_player = handle_no_valid_moves(stdscr, board, current_player)
            print_board(stdscr, board, cursor_row, cursor_col, current_player)


def main():
    wrapper(_main)
