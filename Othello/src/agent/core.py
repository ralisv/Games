from agent.heuristic import evaluate_board, evaluate_move
from game.board import Board
from game.cell import Cell
from game.core import get_scores, get_valid_moves, is_game_over
from game.position import Position
from game.rules import is_valid_move
from game.utils import get_opposing_player

INFINITY = 10**10


def pick_best_turn(board: Board, player: Cell) -> Position:
    """
    Pick the best turn for the current player.

    There MUST be at least one valid move for the current player.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.
        cursor (Position): The cursor position.
    """

    def alpha_beta(current_player: Cell, depth: int, alpha: int, beta: int) -> int:
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
            score = get_scores(board)
            return score[current_player] - score[get_opposing_player(current_player)]

        if current_player == player:
            value = -INFINITY
            for move in sorted(
                get_valid_moves(board, current_player),
                key=lambda move: evaluate_move(board, move, current_player),
            ):
                board.put_disc(move, current_player)
                value = max(
                    value,
                    alpha_beta(
                        get_opposing_player(current_player), depth - 1, alpha, beta
                    ),
                )
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
                value = min(
                    value,
                    alpha_beta(
                        get_opposing_player(current_player), depth - 1, alpha, beta
                    ),
                )
                beta = min(beta, value)
                board.undo()
                if alpha >= beta:
                    break
            return value

    best_score = -INFINITY
    best_move = Position(
        0, 0
    )  # Dummy move, this will be replaced if there are valid moves
    for move in get_valid_moves(board, player):
        board.put_disc(move, player)
        score = alpha_beta(get_opposing_player(player), 3, -INFINITY, INFINITY)
        board.undo()
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
