from agent.utils import evaluate_board
from game.board import Board
from game.cell import Cell
from game.core import get_valid_moves
from game.position import Position
from game.rules import is_valid_move


def pick_best_turn(board: Board, current_player: Cell) -> Position:
    """
    Make a turn for the current player.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.
        cursor (Position): The cursor position.
    """

    return max(
        get_valid_moves(board, current_player),
        key=lambda move: evaluate_board(board, current_player),
    )
