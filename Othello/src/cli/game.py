import curses
from time import sleep

from board import Board, Cell
from game import is_valid_move, put_disc
from game.rules import can_move, is_game_over

from .core import *


def _main(stdscr):
    initialize_screen(stdscr)

    current_player: Cell = Cell.BLACK
    cursor_row, cursor_col = 0, 0

    board = Board(8, 8)

    while True:
        while not check_terminal_size(stdscr, board):
            try:
                stdscr.clear()
                print_top_info(stdscr, "Terminal size is too small")
            except curses.error:
                pass  # If even this fails, we can't do much
            sleep(0.1)

        if is_game_over(board):
            print_top_info(stdscr, "Game over")
            hide_cursor(stdscr, board, cursor_row, cursor_col)
            stdscr.refresh()
            sleep(60)
            break

        if not can_move(board, current_player):
            stdscr.clear()
            print_top_info(
                stdscr, f"No valid moves left for {current_player.name}, skipping turn"
            )
            sleep(1)

            current_player = Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK

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
