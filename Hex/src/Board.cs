using System;
using System.Collections.Generic;
using System.Linq;


public enum PlayerId { One, Two }


public class Game
{
    /// <summary>
    /// Random number generator.
    /// </summary>
    static readonly Random random = new();

    public readonly int width;

    public readonly int height;

    /// <summary>
    /// The game board, indexed by row and column.
    /// </summary>
    public readonly Hexagon[,] board;

    /// <summary>
    /// Set of coordinates of free fields.
    /// </summary>
    HashSet<(int, int)> freeFields;

    /// <summary>
    /// The player that is currently playing or the player that won the game, if IsOver is true.
    /// </summary>
    public PlayerId CurrentPlayer { get; private set; } = PlayerId.Two;

    bool _isOver = false;

    /// <summary>
    /// True if the game is over, false otherwise. In case of a draw, the player that played last wins.
    /// </summary>
    public bool IsOver
    {
        get => _isOver;
        set
        {
            _isOver = value;
        }
    }

    /// <summary>
    /// Stack of moves, used for undoing moves.
    /// </summary>
    private readonly Stack<(int, int)> history = new();

    /// <summary>
    /// Returns border identifier to distinguish between opposite borders.
    /// </summary>
    /// <param name="hexCoords">Coordinates of the hexagon</param>
    /// <returns>integer representing the border</returns>
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
                // Initialize hexagon and borders
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

    /// <summary>
    /// Predicate to check if the given coordinates are within the bounds of the board.
    /// </summary>
    /// <param name="row"></param>
    /// <param name="col"></param>
    /// <returns>true if the given coordinates are within the bounds of the board, false otherwise</returns>
    public bool IsInBounds(int row, int col)
    {
        return row >= 0 && row < height && col >= 0 && col < width;
    }

    /// <summary>
    /// Plays a move for the current player at the given coordinates.
    /// </summary>
    /// <param name="row">row index</param>
    /// <param name="col">column index</param>
    /// <returns>true if the turn was valid, false otherwise</returns>
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

    /// <summary>
    /// Undoes the last move, single Play operation.
    /// </summary>
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

    /// <summary>
    /// Searches the board for all possible moves.
    /// </summary>
    /// <returns>List of all possible moves in the current state of the game</returns>
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

    /// <summary>
    /// Beware, this method has linear time complexity.
    /// </summary>
    /// <returns>Returns a random possible move</returns>
    public (int, int)? RandomPossibleMove()
    {
        if (freeFields.Count == 0)
        {
            return null;
        }
        return freeFields.ElementAt(random.Next(freeFields.Count));
    }
}
