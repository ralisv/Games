import random
from typing import List

import numpy as np


def is_valid(board: np.ndarray, row: int, col: int, num: int) -> bool:
    # Check the number in the row
    if num in board[row]:
        return False

    # Check the number in the column
    if num in board[:, col]:
        return False

    # Check the number in the box
    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


def solve_sudoku(board: np.ndarray) -> bool:
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku(board):
                            return True
                        board[i][j] = 0
                return False
    return True


def generate_sudoku() -> np.ndarray:
    board: np.ndarray = np.zeros((9, 9), dtype=int)
    # Fill the diagonal 3x3 matrices
    for i in range(0, 9, 3):
        for j in range(i, i + 3):
            for k in range(i, i + 3):
                while True:
                    num: int = random.randint(1, 9)
                    if is_valid(board, j, k, num):
                        board[j][k] = num
                        break
    # Solve the partially filled board
    solve_sudoku(board)
    return board


print(generate_sudoku())
