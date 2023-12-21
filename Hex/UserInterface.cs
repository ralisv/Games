using System.Text;


static class UI
{
    static string RED = "\u001b[31m";
    static string BLUE = "\u001b[34m";

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
                    sb.Append($"{hex.Value}");
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