from agent.heuristic import evaluate_board, evaluate_move
from game.board import Board
from game.cell import Cell
from game.core import get_valid_moves, is_game_over
from game.position import Position
from game.rules import is_valid_move

INFINITY = 10**10


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
        key=lambda move: alpha_beta(board, current_player, 3, -INFINITY, INFINITY),
    )


def alpha_beta(
    board: Board, current_player: Cell, depth: int, alpha: int, beta: int
) -> int:
    """
    Alpha-beta pruning algorithm.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.
        depth (int): The depth of the search tree.
        alpha (int): The alpha value.
        beta (int): The beta value.

    Returns:
        int: The best score.
    """
    if depth == 0 or is_game_over(board):
        return evaluate_board(board, current_player)

    if current_player == Cell.WHITE:
        value = -INFINITY
        for move in sorted(
            get_valid_moves(board, current_player),
            key=lambda move: evaluate_move(board, move, current_player),
        ):
            board.put_disc(move, current_player)
            value = max(value, alpha_beta(board, Cell.BLACK, depth - 1, alpha, beta))
            alpha = max(alpha, value)
            board.undo()
            if alpha >= beta:
                break
        return value
    else:
        value = INFINITY
        for move in sorted(
            get_valid_moves(board, current_player),
            key=lambda move: evaluate_move(board, move, current_player),
        ):
            board.put_disc(move, current_player)
            value = min(value, alpha_beta(board, Cell.WHITE, depth - 1, alpha, beta))
            beta = min(beta, value)
            board.undo()
            if alpha >= beta:
                break
        return value
