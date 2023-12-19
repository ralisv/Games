using System.Collections.Generic;
using System.Text;

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

    public readonly List<List<PlayerSymbol?>> Board;

    public PlayerSymbol CurrentPlayer { get; private set; }

    private Stack<int> history;


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

        history = new();

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

        history.Push(col);

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

    int CountCellsInDirection(int row, int col, int rowDelta, int colDelta)
    // Checks how many players cells are in the direction specified by Delta
    {
        int count = 0;
        for (int i = 1; i < 4; i++)
        {
            int newRow = row + rowDelta * i;
            int newCol = col + colDelta * i;

            if (!IsInBounds(newRow, newCol))
            {
                break;
            }

            PlayerSymbol? cell = Board[newRow][newCol];

            if (cell == CurrentPlayer)
            {
                count++;
                continue;
            }
            break;
        }
        return count;
    }

    bool CheckCells(int row, int col, int rowDelta, int colDelta)
    // Checks cells in both the direction specified by Delta and the opposite direction
    {
        int playerCellsInLine = 1 + CountCellsInDirection(row, col, rowDelta, colDelta)
            + CountCellsInDirection(row, col, -rowDelta, -colDelta);
        return playerCellsInLine == WinningLength;
    }

    public void Undo() {
        if (history.Count == 0) {
            throw new System.InvalidOperationException("No moves to undo.");
        }

        int col = history.Pop();
        for (int row = 0; row < Height; row++) {
            if (Board[row][col] != null) {
                Board[row][col] = null;
                break;
            }
        }
        CurrentPlayer = CurrentPlayer == PlayerSymbol.X ? PlayerSymbol.O : PlayerSymbol.X;
    }
}
