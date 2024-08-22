import curses
from time import sleep

from board.cell import Cell
from cli.core import *
from game.core import put_disc
from game.rules import is_valid_move


def _main(stdscr):
    initialize_screen(stdscr)

    board = initialize_board()
    current_player: Cell = Cell.BLACK
    cursor_row, cursor_col = 0, 0

    while True:
        while not check_terminal_size(stdscr, board):
            try:
                stdscr.clear()
                print_top_info(stdscr, "Terminal size is too small")
            except curses.error:
                pass  # If even this fails, we can't do much
            sleep(0.1)

        print_top_info(stdscr, f"Current player: {current_player.name}")
        print_board(stdscr, board, cursor_row, cursor_col, current_player)

        key = stdscr.getch()
        if key == ord("q"):
            break

        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            cursor_row, cursor_col = move_cursor(
                stdscr, board, key, cursor_row, cursor_col, current_player
            )

        if key in [ord(" "), 10]:
            if is_valid_move(board, cursor_row, cursor_col, current_player):
                put_disc(board, cursor_row, cursor_col, current_player)
                current_player = (
                    Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK
                )
            else:
                continue


def main():
    curses.wrapper(_main)
