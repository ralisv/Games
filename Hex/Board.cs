using System;
using System.Collections.Generic;


public enum PlayerId { One, Two }


public class Game
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

    private readonly Stack<Hexagon> history = new();

    public Game(int width, int height)
    {
        this.width = width;
        this.height = height;

        // Initialize board
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
        if (hex.Owner != null)
        {
            return false;
        }

        history.Push(hex);
        hex.Owner = CurrentPlayer;
        IsOver = hex.Connects();
        if (!IsOver)
        {
            CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        }
        return true;
    }

    public void Undo() {
        if (IsOver) {
            IsOver = false;
        }
        else {
            CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        }
        history.Pop().Owner = null;
    }

    public List<Hexagon> PossibleMoves()
    {
        List<Hexagon> moves = new();
        foreach (var hex in board)
        {
            if (hex.Owner == null)
            {
                moves.Add(hex);
            }
        }
        return moves;
    }
}