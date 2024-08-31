from game.board import Board
from game.cell import Cell
from game.position import Position
from game.utils import neighbors


def evaluate_board(board: Board, current_player: Cell) -> int:
    """
    Evaluate the board for the current player.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.

    Returns:
        int: The board evaluation.
    """
    score = 0

    for row in range(board.height):
        for col in range(board.width):
            score += evaluate_cell(board, Position(row, col), current_player)

    return score


def evaluate_cell(board: Board, position: Position, current_player: Cell) -> int:
    """
    Evaluate the cell for the current player.

    Args:
        board (Board): The game board.
        position (Position): The cell to evaluate.
        current_player (Cell): The player who is making the move.

    Returns:
        int: The cell evaluation.
    """
    safe_directions = 0
    for neighbor, direction in filter(
        lambda pos: board.is_in_bounds(pos[0]) and board.is_in_bounds(pos[1]),
        neighbors(position.row, position.col),
    ):
        while board[neighbor.row][neighbor.col] == current_player:
            neighbor = Position(
                neighbor.row + direction.row, neighbor.col + direction.col
            )
            if not board.is_in_bounds(neighbor):
                safe_directions += 1
                break

    return safe_directions


def evaluate_move(board: Board, move: Position, current_player: Cell) -> int:
    """
    Evaluate the move for the current player.

    Args:
        board (Board): The game board.
        move (Position): The move to evaluate.
        current_player (Cell): The player who is making the move.

    Returns:
        int: The move evaluation.
    """

    board.put_disc(move, current_player)
    score = evaluate_board(board, current_player)
    board.undo()
    return score
