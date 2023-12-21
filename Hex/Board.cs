using System;


class Game
{
    public readonly int width;
    public readonly int height;

    public readonly Hexagon[,] board;

    public PlayerId CurrentPlayer { get; private set; } = PlayerId.One;


    public Game(int width, int height)
    {
        this.width = width;
        this.height = height;

        board = new Hexagon[width, height];
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++)
            {
                board[row, col] = new Hexagon();
            }
        }

        // Set neighbors
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++)
            {
                for (int i = 0; i < 6; i++)
                {
                    var (rowDelta, colDelta) = Hexagon.AdjacentCoords[i];
                    var neighborRow = row + rowDelta;
                    var neighborCol = col + colDelta;
                    if (IsInBounds(neighborRow, neighborCol))
                    {
                        board[row, col].neighbors[i] = board[neighborRow, neighborCol];
                    }
                }
            }
        }
    }

    public bool IsInBounds(int row, int col)
    {
        return row >= 0 && row < height && col >= 0 && col < width;
    }

    public bool Play(int row, int col) {
        if (!IsInBounds(row, col)) {
            return false;
        }

        var hex = board[row, col];
        if (hex.Value != null) {
            return false;
        }

        hex.Value = CurrentPlayer;
        CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        return true;
    }

}