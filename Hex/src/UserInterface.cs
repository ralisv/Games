using System.Linq;
using System.Text;
using System;


static class UI
{
    readonly static string PlayerSymbol = "●";
    readonly static string CursorSymbol = "🞋";
    readonly static string EmptySymbol = "·";

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

        for (int row = 0; row < game.height; row++)
        {
            sb.Append(' ', row);

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
            sb.AppendLine();
        }

        return sb.ToString();
    }
    public static string Cell (Game game, int cursorRow, int cursorCol, int row, int col)
    {
        if (Util.InCorner((row, col), game.width, game.height))
        {
            return $" ";
        }
        var hex = game.board[row, col];
        bool isAdjacentToCursor = Util.IsAdjacentToCursor(cursorRow, cursorCol, row, col);
        if (hex.Owner != null)
        {
            return $"{Player(hex.Owner.Value, highlight: isAdjacentToCursor)}";
        }
        else
        {
            return $"{(isAdjacentToCursor ? Color.LightGrey : Color.Grey)}{EmptySymbol}{Color.Reset}";
        }
    }

    public static string Player(PlayerId player, bool highlight = false)
    {
        switch(player)
        {
            case PlayerId.One:
                return $"{(highlight ? Color.LightRed : Color.Red)}{PlayerSymbol}{Color.Reset}";
            case PlayerId.Two:
                return $"{(highlight ? Color.LightBlue : Color.Blue)}{PlayerSymbol}{Color.Reset}";
            default:
                throw new Exception("Invalid player");
        }
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
}