using System.Text;
using System.Collections.Generic;

static class UI
{
    static string EmptyCell = "  ";
    static string RedCell = "🔴";
    static string BlueCell = "🔵";
    static string LinePrefix = "┃";
    static string LineSuffix = "┃";
    static string BoardSeparator = "━━";
    static string BoardTopLeft = "┏";
    static string BoardTopRight = "┓";
    static string BoardBottomLeft = "┗";
    static string BoardBottomRight = "┛";
    static string BoardLeftT = "┣";
    static string BoardRightT = "┫";
    static string Aim = "・";
    public static string Player(PlayerSymbol player)
    {
        return player == PlayerSymbol.X ? RedCell : BlueCell;
    }

    public static string Cell(PlayerSymbol? cell)
    {
        return cell == null ? EmptyCell : Player(cell.Value);
    }

    public static string Game(Game game, int currentCol)
    {
        StringBuilder sb = new StringBuilder();

        // Print the top border
        sb.Append(BoardTopLeft);
        for (int i = 0; i < game.Width; i++)
        {
            sb.Append(BoardSeparator);
        }
        sb.Append(BoardTopRight);
        sb.AppendLine();

        // Print the current player's symbol at the specified column index
        sb.Append(LinePrefix);
        for (int i = 0; i < game.Width; i++)
        {
            sb.Append(i == currentCol ? Player(game.CurrentPlayer) : EmptyCell);
        }
        sb.Append(LineSuffix);
        sb.AppendLine();

        // Print the separator
        sb.Append(BoardLeftT);
        for (int i = 0; i < game.Width; i++)
        {
            sb.Append(BoardSeparator);
        }
        sb.Append(BoardRightT);
        sb.AppendLine();

        // Print the board
        sb.Append(Board(game.Board, currentCol));

        // Print the bottom border
        sb.Append(BoardBottomLeft);
        for (int i = 0; i < game.Width; i++)
        {
            sb.Append(BoardSeparator);
        }
        sb.Append(BoardBottomRight);
        sb.AppendLine();

        return sb.ToString();
    }

    public static string Board(List<List<PlayerSymbol?>> board, int currentCol)
    {
        StringBuilder sb = new();

        // Print the current player's symbol at the specified column index
        for (int row = 0; row < board.Count; row++)
        {
            sb.Append(LinePrefix);
            for (int col = 0; col < board[0].Count; col++)
            {
                var cell = board[row][col];
                if (col == currentCol && cell == null && row % 2 == 1)
                {
                    sb.Append(Aim);
                }
                else
                {
                    sb.Append(Cell(cell));
                }
            }
            sb.Append(LineSuffix);
            sb.AppendLine();
        }
        return sb.ToString();
    }
}
