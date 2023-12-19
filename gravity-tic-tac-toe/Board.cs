using System.Collections.Generic;
using System;

static class UI { }

enum PlayResult
{
    Again,
    Draw,
    Win,
    Next,
}

class Game
{
    public readonly int Height;
    public readonly int Width;

    public readonly int WinningLength;

    private readonly List<List<PlayerSymbol?>> Board;

    public PlayerSymbol CurrentPlayer { get; private set; }

    public Game(int height, int width, PlayerSymbol startingPlayer = PlayerSymbol.X, int winningLength = 4)
    {
        Height = height;
        Width = width;
        Board = new();

        for (int row = 0; row < Height; row++)
        {
            Board.Add(new());
            for (int col = 0; col < Width; col++)
            {
                Board[row].Add(null);
            }
        }

        CurrentPlayer = startingPlayer;
        WinningLength = winningLength;
    }

    bool IsInBounds(int row, int col)
    {
        return row >= 0 && row < Height && col >= 0 && col < Width;
    }

    bool IsDraw()
    {
        for (int col = 0; col < Width; col++)
        {
            if (Board[0][col] == null)
            {
                return false;
            }
        }
        return true;
    }

    public PlayResult Play(int col)
    {
        if (!IsInBounds(0, col) | Board[0][col] != null)
        {
            return PlayResult.Again;
        }

        int row;
        for (row = Height - 1; row >= 0; row--)
        {
            if (Board[row][col] == null)
            {
                Board[row][col] = CurrentPlayer;
                break;
            }
        }

        if (HasWon(row, col))
        {
            return PlayResult.Win;
        }

        if (IsDraw())
        {
            return PlayResult.Draw;
        }

        CurrentPlayer = CurrentPlayer == PlayerSymbol.X ? PlayerSymbol.O : PlayerSymbol.X;
        return PlayResult.Next;
    }

    bool HasWon(int row, int col)
    {
        return CheckCells(row, col, 1, 0) || CheckCells(row, col, 0, 1) || CheckCells(row, col, 1, 1) || CheckCells(row, col, 1, -1);
    }

    bool CheckCells(int row, int col, int rowDelta, int colDelta)
    // Checks cells in both the direction specified by Delta and the opposite direction
    {
        int count = 1;

        var symbol = Board[row][col];
        for (int i = 1; i < 4; i++)
        {
            PlayerSymbol? cell = Board[row + rowDelta * i][col + colDelta * i];

            if (cell == CurrentPlayer)
            {
                count++;
                continue;
            }
            break;
        }

        for (int i = 1; i < 4; i++)
        {
            PlayerSymbol? cell = Board[row - rowDelta * i][col - colDelta * i];

            if (cell == CurrentPlayer)
            {
                count++;
                continue;
            }
            break;
        }

        return count == WinningLength;
    }
}
