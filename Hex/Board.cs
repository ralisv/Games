using System;
using System.Collections.Generic;
using System.Linq;


enum PlayerId { One, Two }


class Game
{
    public readonly int width;
    public readonly int height;

    public readonly Hexagon[,] board;

    public PlayerId CurrentPlayer { get; private set; } = PlayerId.One;

    bool _isOver = false;
    public bool IsOver
    {
        get => _isOver;
        set {
            _isOver = value;
            if (value)
            {
                Console.WriteLine($"Player {CurrentPlayer} wins!");
            }
        }
    }

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

    public bool Play(int row, int col)
    {
        if (!IsInBounds(row, col) || IsOver)
        {
            return false;
        }

        var hex = board[row, col];
        if (hex.Value != null)
        {
            return false;
        }

        hex.Value = CurrentPlayer;
        IsOver = Connects(hex);
        if (!IsOver)
        {
            CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        }
        return true;
    }

    /// <summary>
    /// Returns true if the player owning the hexagon has won, false otherwise.
    /// </summary>
    /// <returns></returns>
    public static bool Connects(Hexagon hex)
    {
        PlayerId player = hex.Value ?? throw new Exception("Hexagon is not owned by a player");
        bool upOrLeft = false;
        bool downOrRight = false;

        // Optimization
        if (!hex.neighbors.Any(hex => hex?.Value == player))
        {
            return false;
        }

        HashSet<Hexagon> visited = new();
        Queue<Hexagon> queue = new();
        queue.Enqueue(hex);
        while (queue.Count > 0)
        {
            var current = queue.Dequeue();
            if (player == PlayerId.One && current.neighbors[0] == null
                || player == PlayerId.Two && current.neighbors[2] == null)
            {
                upOrLeft = true;

            }
            else if (player == PlayerId.One && current.neighbors[5] == null
                || player == PlayerId.Two && current.neighbors[3] == null)
            {
                downOrRight = true;
            }

            if (upOrLeft && downOrRight)
            {
                return true;
            }

            for (int i = 0; i < 6; i++)
            {
                var neighbor = current.neighbors[i];
                if (neighbor != null && visited.Contains(neighbor) == false && neighbor.Value == player)
                {
                    visited.Add(neighbor);
                    queue.Enqueue(neighbor);
                }
            }
        }

        return false;
    }

}