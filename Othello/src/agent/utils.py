from random import randint

from game.board import Board
from game.cell import Cell


def evaluate_board(board: Board, current_player: Cell) -> int:
    """
    Evaluate the board for the current player.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.

    Returns:
        int: The board evaluation.
    """

    return randint(-100, 100)
