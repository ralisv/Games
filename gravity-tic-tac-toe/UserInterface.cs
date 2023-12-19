using System.Text;
using System.Collections.Generic;


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

    public static string Game(Game game, int currentCol)
    {
        StringBuilder sb = new StringBuilder();

        // Print the current player's symbol at the specified column index
        for (int i = 0; i < game.Width; i++)
        {
            sb.Append(i == currentCol ? Player(game.CurrentPlayer) : " ");
        }
        sb.AppendLine();

        sb.Append(Board(game.Board));

        return sb.ToString();
    }

    public static string Board(List<List<PlayerSymbol?>> board)
    {
        StringBuilder sb = new StringBuilder();

        // Print the current player's symbol at the specified column index
        for (int row = 0; row < board.Count; row++)
        {
            for (int col = 0; col < board[0].Count; col++)
            {
                sb.Append(Cell(board[row][col]));
            }
            sb.AppendLine();
        }
        return sb.ToString();
    }

}