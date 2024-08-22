import curses

from board.board import Board
from board.cell import Cell
from cli.constants import AIM

# Define color pair numbers
BLACK_PAIR = 1
WHITE_PAIR = 2


def initialize_screen(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(BLACK_PAIR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(WHITE_PAIR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()


def print_board(stdscr, board, cursor_row, cursor_col, current_player):
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(
        0, 0, f"Current player: {'Black' if current_player == Cell.BLACK else 'White'}"
    )
    for row in range(board.height):
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
                    col * 2,
                    char if char != Cell.EMPTY.value else AIM,
                    curses.color_pair(color_pair) | curses.A_REVERSE,
                )
            else:
                stdscr.addstr(row + 2, col * 2, char)

    stdscr.addstr(
        height - 1,
        0,
        "Use arrow keys to move, Enter or Space to place disc, 'q' to quit",
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
        stdscr.addstr(cursor_row + 2, cursor_col * 2, old_char)

        # Draw new cursor position
        new_char = (
            AIM
            if board[new_row][new_col] == Cell.EMPTY
            else board[new_row][new_col].value
        )
        color_pair = BLACK_PAIR if current_player == Cell.BLACK else WHITE_PAIR
        stdscr.addstr(
            new_row + 2,
            new_col * 2,
            new_char,
            curses.color_pair(color_pair) | curses.A_REVERSE,
        )

        # Update current player info
        stdscr.addstr(
            0,
            0,
            f"Current player: {'Black' if current_player == Cell.BLACK else 'White'}",
        )

        stdscr.refresh()

    return new_row, new_col


def handle_no_valid_moves(stdscr, board, current_player):
    stdscr.addstr(board.height + 3, 0, f"No valid moves for {current_player}")
    stdscr.refresh()
    stdscr.getch()  # Wait for a key press
    return Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK


def initialize_board():
    board = Board(8, 8)
    board[3][3] = Cell.WHITE
    board[3][4] = Cell.BLACK
    board[4][3] = Cell.BLACK
    board[4][4] = Cell.WHITE
    return board
