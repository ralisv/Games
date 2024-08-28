import curses
import sys

from game.board import Board
from game.cell import Cell

from .constants import BLACK_DISC, EMPTY, WHITE_DISC


def check_terminal_size(stdscr: curses.window, board: Board) -> bool:
    terminal_height, terminal_width = stdscr.getmaxyx()
    required_height = board.height + 3  # 1 for information at the top, 2 for borders
    required_width = board.width * 2 + 2  # 2 chars per cell, 2 for borders

    return terminal_height >= required_height and terminal_width >= required_width


def get_cell_char(cell: Cell) -> str:
    mapping = {Cell.BLACK: BLACK_DISC, Cell.WHITE: WHITE_DISC, Cell.EMPTY: EMPTY}
    return mapping[cell]


def against_bot() -> bool:
    return sys.argv[1] == "--bot" if len(sys.argv) > 1 else False
