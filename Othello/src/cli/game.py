import curses
from time import sleep

from agent import pick_best_turn
from game.board import Board
from game.cell import Cell
from game.core import can_play, get_scores, is_game_over
from game.position import Position
from game.rules import is_valid_move
from game.utils import get_opposing_player

from .core import *
from .utils import against_bot, check_terminal_size


def _main(stdscr: curses.window):
    initialize_screen(stdscr)

    plays_against_bot = against_bot()

    current_player: Cell = Cell.BLACK
    cursor = Position(0, 0)

    board = Board(8, 8)

    while not is_game_over(board):
        while not check_terminal_size(stdscr, board):
            try:
                stdscr.clear()
                print_top_info(stdscr, "Terminal size is too small")
            except curses.error:
                pass  # If even this fails, we can't do much
            sleep(0.1)

        if not can_play(board, current_player):
            stdscr.clear()
            print_top_info(
                stdscr, f"No valid moves left for {current_player.name}, skipping turn"
            )
            sleep(2)
            current_player = get_opposing_player(current_player)
            continue

        print_top_info(stdscr, f"Current player: {current_player.name}")
        print_board(stdscr, board, cursor, current_player)

        if plays_against_bot and current_player == Cell.WHITE:
            new_cursor = pick_best_turn(board, current_player)
            update_cursor(stdscr, board, new_cursor, cursor, current_player)
            sleep(1)

            cursor = new_cursor
            board.put_disc(cursor, current_player)
            current_player = get_opposing_player(current_player)
            continue

        key = stdscr.getch()

        match key:
            case 113:  # q
                return
            case 32 | 10:  # Space or Enter
                if is_valid_move(board, cursor, current_player):
                    board.put_disc(cursor, current_player)
                    current_player = get_opposing_player(current_player)
                continue
            case curses.KEY_UP:
                new_cursor = Position(cursor.row - 1, cursor.col)
            case curses.KEY_DOWN:
                new_cursor = Position(cursor.row + 1, cursor.col)
            case curses.KEY_LEFT:
                new_cursor = Position(cursor.row, cursor.col - 1)
            case curses.KEY_RIGHT:
                new_cursor = Position(cursor.row, cursor.col + 1)
            case _:
                continue
        cursor = update_cursor(stdscr, board, new_cursor, cursor, current_player)

    print_top_info(stdscr, "Game over")
    print_board(stdscr, board, cursor, current_player)
    hide_cursor(stdscr, board, cursor)
    stdscr.refresh()
    sleep(2)

    scores = get_scores(board)
    print_top_info(stdscr, f"White: {scores[Cell.WHITE]}, Black: {scores[Cell.BLACK]}")
    sleep(60)


def main(against_bot: bool = False) -> None:
    curses.wrapper(_main)
