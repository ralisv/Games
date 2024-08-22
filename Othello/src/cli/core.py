import curses

from board import Board, Cell

from .constants import *

# Define color pair numbers
BLACK_PAIR = 1
WHITE_PAIR = 2


def initialize_screen(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(
        BLACK_PAIR, curses.COLOR_WHITE, curses.COLOR_BLACK
    )  # White text on black background
    curses.init_pair(
        WHITE_PAIR, curses.COLOR_BLACK, curses.COLOR_WHITE
    )  # Black text on white background
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()


def check_terminal_size(stdscr, board):
    terminal_height, terminal_width = stdscr.getmaxyx()
    required_height = board.height + 3  # 1 for information at the top, 2 for borders
    required_width = (
        board.width * 2 + 3
    )  # 2 chars per cell, 2 for borders, 1 for safety

    if terminal_height < required_height or terminal_width < required_width:
        return False
    return True


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
            char = Cell.EMPTY.value
            if board[row][col] == Cell.BLACK:
                char = Cell.BLACK.value
            elif board[row][col] == Cell.WHITE:
                char = Cell.WHITE.value

            if row == cursor_row and col == cursor_col:
                color_pair = BLACK_PAIR if current_player == Cell.BLACK else WHITE_PAIR
                stdscr.addstr(
                    row + 2,
                    col * 2 + 1,
                    char if char != Cell.EMPTY.value else AIM,
                    curses.color_pair(color_pair),
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
        old_char = board[cursor_row][cursor_col].value
        stdscr.addstr(cursor_row + 2, cursor_col * 2 + 1, old_char)

        # Draw new cursor position
        new_char = (
            AIM
            if board[new_row][new_col] == Cell.EMPTY
            else board[new_row][new_col].value
        )
        color_pair = BLACK_PAIR if current_player == Cell.BLACK else WHITE_PAIR
        stdscr.addstr(
            new_row + 2,
            new_col * 2 + 1,
            new_char,
            curses.color_pair(color_pair),
        )

        # Update current player info
        stdscr.addstr(
            0,
            0,
            f"Current player: {'Black' if current_player == Cell.BLACK else 'White'}",
        )

        stdscr.refresh()

    return new_row, new_col


def hide_cursor(stdscr, board: Board, cursor_row: int, cursor_col: int):
    stdscr.addstr(
        cursor_row + 2, cursor_col * 2 + 1, board[cursor_row][cursor_col].value
    )
