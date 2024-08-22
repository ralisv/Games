import curses
from time import sleep

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


def check_terminal_size(stdscr, board):
    terminal_height, terminal_width = stdscr.getmaxyx()
    required_height = (
        board.height + 4
    )  # 1 for player info, 2 for borders, 1 for instructions
    required_width = (
        board.width * 2 + 3
    )  # 2 chars per cell, 2 for borders, 1 for safety

    if terminal_height < required_height or terminal_width < required_width:
        stdscr.clear()
        top_info = "Terminal too small. Please resize."
        padded_top_info = top_info + " " * (terminal_width - len(top_info) - 1)
        try:
            stdscr.addstr(0, 0, padded_top_info[: terminal_width - 1])
        except curses.error:
            pass  # If even this fails, we can't do much
        stdscr.refresh()
        return False
    return True


def _main(stdscr):
    initialize_screen(stdscr)

    board = initialize_board()
    current_player: Cell = Cell.BLACK
    cursor_row, cursor_col = 0, 0

    # Check terminal size before printing the board for the first time
    while not check_terminal_size(stdscr, board):
        sleep(0.1)

    print_board(stdscr, board, cursor_row, cursor_col, current_player)

    while True:
        # Check terminal size at the beginning of each loop
        while not check_terminal_size(stdscr, board):
            sleep(0.1)

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
    curses.wrapper(_main)
