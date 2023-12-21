using System;


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

    private PlayerId? _value = null;
    public PlayerId? Value
    {
        get
        {
            return _value;
        }
        set
        {
            if (_value != null)
            {
                throw new Exception("Hexagon is already owned by a player");
            }
            _value = value;
        }
    }

    public Hexagon?[] neighbors = new Hexagon[6];
}