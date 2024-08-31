import curses

from game.board import Board
from game.cell import Cell
from game.core import get_valid_moves
from game.position import Position

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
    cursor: Position,
    current_player: Cell,
) -> None:
    """
    Print the game board on the screen.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        cursor (Position): Position of the cursor.
        current_player (Cell): The current player.
    """
    # Print top border
    stdscr.addstr(
        1, 0, TOP_LEFT_EDGE_LINE + HORIZONTAL_LINE * board.width + TOP_RIGHT_EDGE_LINE
    )

    valid_moves = set(get_valid_moves(board, current_player))

    for row in range(board.height):
        stdscr.addstr(row + 2, 0, VERTICAL_LINE)  # Left border
        for col in range(board.width):
            cell = board[row][col]
            char = get_cell_char(cell)

            if Position(row, col) in valid_moves and cell == Cell.EMPTY:
                char = VALID_MOVE_MARK

            if Position(row, col) == cursor:
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
    new_cursor: Position,
    current_cursor: Position,
    current_player: Cell,
) -> Position:
    """
    Move the cursor on the screen to the new position.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        new_cursor (Position): The new position of the cursor.
        current_cursor (Position): The current position of the cursor.
        current_player (Cell): The current player.

    Returns:
        Position: The new position of the cursor if valid, otherwise the current position.
    """
    if board.is_in_bounds(new_cursor) and new_cursor != current_cursor:
        # Clear old cursor position
        old_char = get_cell_char(board[current_cursor.row][current_cursor.col])
        stdscr.addstr(current_cursor.row + 2, current_cursor.col * 2 + 1, old_char)

        # Draw new cursor position
        new_char = get_cell_char(board[new_cursor.row][new_cursor.col])
        stdscr.addstr(
            new_cursor.row + 2,
            new_cursor.col * 2 + 1,
            new_char,
            curses.color_pair(current_player.value),
        )

        stdscr.refresh()
        return new_cursor

    return current_cursor


def hide_cursor(stdscr: curses.window, board: Board, cursor: Position) -> None:
    """
    Hide the game's cursor from the screen.

    Args:
        stdscr (curses.window): The standard screen window.
        board (Board): The game board.
        cursor (Position): Position of the cursor.
    """
    stdscr.addstr(
        cursor.row + 2, cursor.col * 2 + 1, get_cell_char(board[cursor.row][cursor.col])
    )
