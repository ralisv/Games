using System.Text;


static class UI
{
    static string RED = "\x1b[38;2;247;50;50m";
    static string BLUE = "\x1b[38;2;0;127;255m";

    public static string Game(Game game)
    {
        var sb = new StringBuilder();
        for (int row = 0; row < game.height; row++)
        {
            sb.Append(' ', row);
            for (int col = 0; col < game.width; col++)
            {
                sb.Append(" ");
                var hex = game.board[row, col];
                if (hex.Value == null)
                {
                    sb.Append(".");
                }
                else
                {
                    sb.Append(Player(hex.Value.Value));
                }
            }
            sb.AppendLine();
        }

        return sb.ToString();
    }

    public static string Player(PlayerSymbol player)
    {
        if (player == PlayerSymbol.X)
        {
            return RED + "O" + "\u001b[0m";
        }
        else if (player == PlayerSymbol.O)
        {
            return BLUE + "O" + "\u001b[0m";
        }
        else
        {
            return " ";
        }
    }
}