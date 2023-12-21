using System;


class Game {
    readonly int width;
    readonly int height;

    public readonly Hexagon[,] board;

    public Game(int width, int height)
    {
        this.width = width;
        this.height = height;

        board = new Hexagon[width, height];
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++) {
                board[row, col] = new Hexagon();
            }
        }

        // Set neighbors
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++) {
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



}