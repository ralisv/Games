using System.Collections.Generic;


enum PlayerSymbol
{
    X,
    O
}


enum PlayResult
{
    Again,
    Draw,
    Win,
    Next,
}

/// <summary>
/// Represents a game of Connect Four
/// </summary>
class Game
{
    /// <summary>
    /// Number of rows.
    /// </summary>
    public readonly int Height;

    /// <summary>
    /// Number of columns.
    /// </summary>
    public readonly int Width;

    /// <summary>
    /// Number of consecutive symbols needed to win.
    /// </summary>
    public readonly int WinningLength;

    /// <summary>
    /// The board of the game, carries information about the state of the game.
    /// </summary>
    public readonly List<List<PlayerSymbol?>> Board;

    /// <summary>
    /// The player whose turn it is.
    /// </summary>
    public PlayerSymbol CurrentPlayer { get; private set; }

    /// <summary>
    /// Stack carrying the history of moves, top of the stack is the most recently used column.
    /// </summary>
    private Stack<int> history;

    /// <summary>
    /// Whether the game has finished.
    /// </summary>
    public bool Finished { get; private set; } = false;

    /// <summary>
    /// Creates a new game.
    /// </summary>
    /// <param name="height"> Number of rows. </param>
    /// <param name="width"> Number of columns. </param>
    /// <param name="startingPlayer"> Player who will have the first turn. </param>
    /// <param name="winningLength"> Number of consecutive symbols needed to win. </param>
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

    /// <summary>
    /// Informs about the result of the game.
    /// </summary>
    /// <returns> true if game resulted in draw, false otherwise </returns>
    public bool IsDraw()
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

    /// <summary>
    /// Drops the current player's symbol in the specified column.
    /// </summary>
    /// <param name="col">Columns index belonging to [0, Width)</param>
    /// <returns> Result of operation </returns>
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
            Finished = true;
            return PlayResult.Win;
        }

        if (IsDraw())
        {
            Finished = true;
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

    /// <summary>
    /// Undoes the most recently made move.
    /// </summary>
    /// <exception cref="System.InvalidOperationException"></exception>
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

        if (Finished)
        {
            Finished = false;
            return;
        }

        CurrentPlayer = CurrentPlayer == PlayerSymbol.X ? PlayerSymbol.O : PlayerSymbol.X;
    }
}
