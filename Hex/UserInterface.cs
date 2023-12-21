using System.Linq;
using System.Text;


static class UI
{
    readonly static string PlayerSymbol = "●";
    readonly static string CursorSymbol = "🞋";
    readonly static string EmptySymbol = "🞄";

    /// <summary>
    /// Returns a string representation of the game board with the cursor at the
    /// given row and column and all neighboring hexagons belonging to the current
    /// player highlighted.
    /// </summary>
    /// <param name="game"></param>
    /// <param name="cursorRow"></param>
    /// <param name="cursorCol"></param>
    /// <returns></returns>
    public static string Game(Game game, int cursorRow, int cursorCol)
    {
        var sb = new StringBuilder();
        // Add top border
        sb.Append(' ', 1);
        for (int i = 0; i < game.width; i++)
        {
            sb.Append(Player(PlayerId.One));
            sb.Append(' ');
        }
        sb.AppendLine();

        for (int row = 0; row < game.height; row++)
        {
            sb.Append(' ', row);

            // Add left border
            sb.Append(Player(PlayerId.Two));
            sb.Append(' ');

            for (int col = 0; col < game.width; col++)
            {
                if (row == cursorRow && col == cursorCol)
                {
                    sb.Append($"{Cursor(game.CurrentPlayer)}");
                }
                else
                {
                    sb.Append($"{Cell(game, cursorRow, cursorCol, row, col)}");
                }
                sb.Append(' ');
            }
            sb.Append(Player(PlayerId.Two)); // Add right border
            sb.AppendLine();
        }
        // Add bottom border
        sb.Append(' ', game.height + 1);
        for (int i = 0; i < game.width; i++)
        {
            sb.Append(Player(PlayerId.One));
            sb.Append(' ');
        }
        return sb.ToString();
    }
    public static string Cell (Game game, int cursorRow, int cursorCol, int row, int col)
    {
        var hex = game.board[row, col];
        bool isAdjacentToCursor = IsAdjacentToCursor(cursorRow, cursorCol, row, col);
        if (hex.Value != null)
        {
            return $"{Player(hex.Value.Value, highlight: isAdjacentToCursor)}";
        }
        else
        {
            return $"{(isAdjacentToCursor ? Color.LightGrey : Color.Grey)}{EmptySymbol}{Color.Reset}";
        }
    }

    public static string Player(PlayerId player, bool highlight = false)
    {
        if (player == PlayerId.One)
        {
            return $"{(highlight ? Color.LightRed : Color.Red)}{PlayerSymbol}{Color.Reset}";
        }
        return $"{(highlight ? Color.LightBlue : Color.Blue)}{PlayerSymbol}{Color.Reset}";
    }

    public static string Cursor(PlayerId player)
    {
        if (player == PlayerId.One)
        {
            return $"{Color.Red}{CursorSymbol}{Color.Reset}";
        }
        else if (player == PlayerId.Two)
        {
            return $"{Color.Blue}{CursorSymbol}{Color.Reset}";
        }
        else
        {
            return " ";
        }
    }

    public static bool IsAdjacentToCursor(int cursorRow, int cursorCol, int row, int col)
    {
        int colDelta = cursorCol - col;
        int rowDelta = cursorRow - row;
        return Hexagon.AdjacentCoords.Contains((rowDelta, colDelta));
    }
}