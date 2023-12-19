using System.Text;


static class UI
{
    public static string Player(PlayerSymbol player)
    {
        return player == PlayerSymbol.X ? "X" : "O";
    }

    public static string Cell(PlayerSymbol? cell)
    {
        return cell == null ? " " : Player(cell.Value);
    }

    public static string Game(PlayerSymbol?[][] board, int currentCol)
    {
        StringBuilder sb = new StringBuilder();

        // Print the current player's symbol at the specified column index
        for (int i = 0; i < board[0].Length; i++)
        {
            sb.Append(i == currentCol ? Player(PlayerSymbol.X) : " ");
        }
        sb.AppendLine();

        sb.Append(Board(board));

        return sb.ToString();
    }

    public static string Board(PlayerSymbol?[][] board)
    {
        StringBuilder sb = new StringBuilder();

        // Print the current player's symbol at the specified column index
        for (int row = 0; row < board.Length; row++)
        {
            for (int col = 0; col < board[0].Length; col++)
            {
                sb.Append(Cell(board[row][col]));
            }
            sb.AppendLine();
        }
        return sb.ToString();
    }

}