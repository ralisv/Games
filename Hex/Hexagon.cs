using System;
using System.Collections.Generic;
using System.Linq;


public class Hexagon
{
    /// <summary>
    /// The six directions that a hexagon can be in relation to another hexagon,
    /// starting at the top left, going to the bottom right, corresponding to the
    /// index of the neighbor in the neighbors array. First element is the row.
    /// </summary>
    public static readonly (int, int)[] AdjacentCoords = new (int, int)[] {
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
    };


    private PlayerId? owner = null;

    /// <summary>
    /// The player that owns the hexagon, or null if it is not owned by any player.
    /// </summary>
    public PlayerId? Owner
    {
        get => owner;
        set
        {
            if (owner != null && value != null)
            {
                throw new Exception("Hexagon is already owned by a player");
            }
            owner = value;
        }
    }

    /// <summary>
    /// Adjacent hexagons, indexed by the direction they are in relation to this hexagon. Or null if there is border.
    /// </summary>
    public Hexagon?[] neighbors = new Hexagon[6];

    /// <summary>
    /// Information about the position of the hexagon on the board. 
    /// </summary>
    /// <returns> true if the hexagon is adjacent to the left or upper border of the board </returns>
    public bool TouchesUpLeft()
    {
        return Owner == PlayerId.One && neighbors[0] == null // up
                || Owner == PlayerId.Two && neighbors[2] == null; // left
    }

    /// <summary>
    /// Information about the position of the hexagon on the board.
    /// </summary>
    /// <returns> true if the hexagon is adjacent to the right or bottom border of the board </returns>
    public bool TouchesDownRight()
    {
        var player = Owner;
        return player == PlayerId.One && neighbors[5] == null // down
                || player == PlayerId.Two && neighbors[3] == null; // right
    }

    /// <summary>
    /// Returns true if the player owning the hexagon has won, false otherwise.
    /// </summary>
    /// <returns></returns>
    public bool Connects()
    {
        PlayerId player = Owner ?? throw new InvalidOperationException("Hexagon is not owned by a player");
        bool upOrLeft = false;
        bool downOrRight = false;

        // Optimization
        if (!neighbors.Any(hex => hex?.Owner == player))
        {
            return false;
        }

        HashSet<Hexagon> visited = new();
        Queue<Hexagon> queue = new();
        queue.Enqueue(this);
        while (queue.Count > 0)
        {
            var current = queue.Dequeue();
            if (current.TouchesUpLeft())
            {
                upOrLeft = true;

            }
            else if (current.TouchesDownRight())
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
                if (neighbor != null && visited.Contains(neighbor) == false && neighbor.Owner == player)
                {
                    visited.Add(neighbor);
                    queue.Enqueue(neighbor);
                }
            }
        }
        return false;
    }
}