import curses

from game.board import Board
from game.cell import Cell

from .constants import *
from .utils import get_cell_char


def initialize_screen(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(Cell.BLACK.value, BLACK_CURSOR_FG, BLACK_CURSOR_BG)
    curses.init_pair(Cell.WHITE.value, WHITE_CURSOR_FG, WHITE_CURSOR_BG)
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()


def print_top_info(stdscr, text: str):
    _, terminal_width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, (text + " " * terminal_width)[: terminal_width - 1])
    stdscr.refresh()


def print_board(stdscr, board, cursor_row, cursor_col, current_player):
    # Print top border
    stdscr.addstr(
        1, 0, TOP_LEFT_EDGE_LINE + HORIZONTAL_LINE * board.width + TOP_RIGHT_EDGE_LINE
    )

    for row in range(board.height):
        stdscr.addstr(row + 2, 0, VERTICAL_LINE)  # Left border
        for col in range(board.width):
            char = get_cell_char(board[row][col])

            if row == cursor_row and col == cursor_col:

                stdscr.addstr(
                    row + 2,
                    col * 2 + 1,
                    char,
                    curses.color_pair(current_player.value),
                )
            else:
                stdscr.addstr(row + 2, col * 2 + 1, char)
        stdscr.addstr(row + 2, board.width * 2 + 1, VERTICAL_LINE)  # Right border

    # Print bottom border
    stdscr.addstr(
        board.height + 2,
        0,
        BOTTOM_LEFT_EDGE_LINE + HORIZONTAL_LINE * board.width + BOTTOM_RIGHT_EDGE_LINE,
    )

    stdscr.refresh()


def move_cursor(stdscr, board, key, cursor_row, cursor_col, current_player):
    new_row, new_col = cursor_row, cursor_col
    if key == curses.KEY_UP and cursor_row > 0:
        new_row -= 1
    elif key == curses.KEY_DOWN and cursor_row < board.height - 1:
        new_row += 1
    elif key == curses.KEY_LEFT and cursor_col > 0:
        new_col -= 1
    elif key == curses.KEY_RIGHT and cursor_col < board.width - 1:
        new_col += 1

    if (new_row, new_col) != (cursor_row, cursor_col):
        # Clear old cursor position
        old_char = get_cell_char(board[cursor_row][cursor_col])
        stdscr.addstr(cursor_row + 2, cursor_col * 2 + 1, old_char)

        # Draw new cursor position
        new_char = get_cell_char(board[new_row][new_col])
        stdscr.addstr(
            new_row + 2,
            new_col * 2 + 1,
            new_char,
            curses.color_pair(current_player.value),
        )

        stdscr.refresh()
    return new_row, new_col


def hide_cursor(stdscr, board: Board, cursor_row: int, cursor_col: int):
    stdscr.addstr(
        cursor_row + 2, cursor_col * 2 + 1, get_cell_char(board[cursor_row][cursor_col])
    )
