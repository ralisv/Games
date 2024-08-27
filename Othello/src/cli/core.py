import curses

from game.board import Board
from game.cell import Cell

from .constants import *
from .utils import get_cell_char


def initialize_screen(stdscr: curses.window) -> None:
    """
    Initialize the screen with the default colors and hide the terminal's cursor.

    Args:
        stdscr (curses.window): The standard screen window.
    """
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(Cell.BLACK.value, BLACK_CURSOR_FG, BLACK_CURSOR_BG)
    curses.init_pair(Cell.WHITE.value, WHITE_CURSOR_FG, WHITE_CURSOR_BG)
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()


def print_top_info(stdscr: curses.window, text: str) -> None:
    """
    Print the information at the top of the screen, text must be a single line
    and can be truncated if the window's width is insufficient.

    Args:
        stdscr (curses.window): The standard screen window.
        text (str): The text to be displayed.
    """
    _, terminal_width = stdscr.getmaxyx()
    stdscr.addstr(0, 0, (text + " " * terminal_width)[: terminal_width - 1])
    stdscr.refresh()


def print_board(
    stdscr: curses.window,
    board: Board,
    cursor_row: int,
    cursor_col: int,
    current_player: Cell,
) -> None:
    """
    Print the game board on the screen.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        cursor_row (int): Row index of the cursor.
        cursor_col (int): Column index of the cursor.
        current_player (Cell): The current player.
    """
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


def update_cursor(
    stdscr: curses.window,
    board: Board,
    key: int,
    cursor_row: int,
    cursor_col: int,
    current_player: Cell,
) -> tuple[int, int]:
    """
    Move the cursor on the screen based on the key pressed.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        key (int): The key pressed by the user.
        cursor_row (int): Row index of the cursor.
        cursor_col (int): Column index of the cursor.
        current_player (Cell): The current player.

    Returns:
        tuple[int, int]: The new row and column index of the cursor.
    """
    new_row, new_col = cursor_row, cursor_col

    match key:
        case curses.KEY_UP:
            new_row -= 1
        case curses.KEY_DOWN:
            new_row += 1
        case curses.KEY_LEFT:
            new_col -= 1
        case curses.KEY_RIGHT:
            new_col += 1

    if board.is_in_bounds(new_row, new_col) and (new_row, new_col) != (
        cursor_row,
        cursor_col,
    ):
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

    return cursor_row, cursor_col


def hide_cursor(
    stdscr: curses.window, board: Board, cursor_row: int, cursor_col: int
) -> None:
    """
    Hide the game's cursor from the screen.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        cursor_row (int): Row index of the cursor.
        cursor_col (int): Column index of the cursor.
    """
    stdscr.addstr(
        cursor_row + 2, cursor_col * 2 + 1, get_cell_char(board[cursor_row][cursor_col])
    )
