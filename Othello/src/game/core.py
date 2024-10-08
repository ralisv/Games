from typing import Generator

from game.position import Position

from .board import Board
from .cell import Cell
from .rules import is_valid_move


def is_game_over(board: Board) -> bool:
    """
    Check if the game is over.

    Args:
        board (Board): The game board.

    Returns:
        bool: True if the game is over, when no valid move can be made by either of the players, False otherwise.
    """
    return not can_play(board, Cell.BLACK) and not can_play(board, Cell.WHITE)


def can_play(board: Board, current_player: Cell) -> bool:
    """
    Check if the current player can make a valid move.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.

    Returns:
        bool: True if the current player can make a valid move, False otherwise.
    """
    return any(
        is_valid_move(board, Position(row, col), current_player)
        for row in range(board.height)
        for col in range(board.width)
    )


def get_valid_moves(
    board: Board, current_player: Cell
) -> Generator[Position, None, None]:
    """
    Get the list of valid moves for the current player.

    Args:
        board (Board): The game board.
        current_player (Cell): The player who is making the move.

    Returns:
        list[Position]: The list of valid moves for the current player.
    """
    return (
        Position(row, col)
        for row in range(board.height)
        for col in range(board.width)
        if is_valid_move(board, Position(row, col), current_player)
    )


def get_scores(board: Board) -> dict[Cell, int]:
    """
    Get the scores of the players by counting the discs.

    Args:
        board (Board): The game board.

    Returns:
        dict[Cell, int]: The scores of the players.
    """
    return {
        Cell.BLACK: sum(row.count(Cell.BLACK) for row in board),
        Cell.WHITE: sum(row.count(Cell.WHITE) for row in board),
    }


def get_opposing_player(current_player: Cell) -> Cell:
    """
    Get the opposing player.

    Args:
        current_player (Cell): The current player.

    Returns:
        Cell: The opposing player.
    """
    return Cell.WHITE if current_player == Cell.BLACK else Cell.BLACK
