using System;
using System.Collections.Generic;
using System.Linq;


public enum PlayerId { One, Two }


public class Game
{
    static readonly Random random = new();

    public readonly int width;
    public readonly int height;

    public readonly Hexagon[,] board;

    HashSet<(int, int)> freeFields;

    public PlayerId CurrentPlayer { get; private set; } = PlayerId.One;

    bool _isOver = false;
    public bool IsOver
    {
        get => _isOver;
        set
        {
            _isOver = value;
        }
    }

    private readonly Stack<(int, int)> history = new();

    int? AssignBorderId((int, int) hexCoords)
    {
        var (row, col) = hexCoords;
        if (row == 0)
        {
            return 0;
        }
        if (row == height - 1)
        {
            return 1;
        }
        if (col == 0)
        {
            return 1;
        }
        if (col == width - 1)
        {
            return 0;
        }
        return null;
    }

    PlayerId? AssignBorderPlayer((int, int) hexCoords)
    {
        var (row, col) = hexCoords;
        if (row == 0)
        {
            return PlayerId.One;
        }
        if (col == 0)
        {
            return PlayerId.Two;
        }
        if (row == height - 1)
        {
            return PlayerId.One;
        }
        if (col == width - 1)
        {
            return PlayerId.Two;
        }
        return null;
    }

    public Game(int width, int height)
    {
        this.width = width;
        this.height = height;
        freeFields = new HashSet<(int, int)>();

        // Initialize board
        board = new Hexagon[width, height];
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++)
            {
                Hexagon current = new(AssignBorderId((row, col)))
                {
                    Owner = AssignBorderPlayer((row, col))
                };
                if (current.Owner == null) {
                    freeFields.Add((row, col));
                }
                board[row, col] = current;
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

        history.Push((row, col));
        freeFields.Remove((row, col));
        hex.Owner = CurrentPlayer;
        IsOver = hex.Connects();
        if (!IsOver)
        {
            CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        }
        return true;
    }

    public void Undo()
    {
        if (IsOver)
        {
            IsOver = false;
        }
        else
        {
            CurrentPlayer = CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
        }
        (int row, int col) = history.Pop();
        freeFields.Add((row, col));
        board[row, col].Owner = null;
    }

    public List<(int, int)> PossibleMoves()
    {
        List<(int, int)> moves = new();
        for (int row = 0; row < width; row++)
        {
            for (int col = 0; col < height; col++)
            {
                if (board[row, col].Owner == null)
                {

                    moves.Add((row, col));
                }
            }
        }
        return moves;
    }

    public (int, int)? RandomPossibleMove()
    {
        if (freeFields.Count == 0)
        {
            return null;
        }
        return freeFields.ElementAt(random.Next(freeFields.Count));
    }
}