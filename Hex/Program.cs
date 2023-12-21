using System;


class Program
{
    static int Main()
    {
        int row = 0;
        int col = 0;
        var game = new Game(7, 7);
        while (true)
        {   
            string PrecalculatedBoard = UI.Game(game, row, col);
            Console.Clear();
            Console.WriteLine(PrecalculatedBoard);

            if (game.IsOver)
            {
                Console.WriteLine($"Player {UI.Player(game.CurrentPlayer)} wins!");
                return 0;
            }

            switch (Console.ReadKey().Key) {
                case ConsoleKey.Q:
                    return 0;
                case ConsoleKey.UpArrow:
                    row = Math.Max(0, row - 1);
                    break;
                case ConsoleKey.DownArrow:
                    row = Math.Min(game.height - 1, row + 1);
                    break;
                case ConsoleKey.LeftArrow:
                    col = Math.Max(0, col - 1);
                    break;
                case ConsoleKey.RightArrow:
                    col = Math.Min(game.width - 1, col + 1);
                    break;
                case ConsoleKey.Spacebar:
                    game.Play(row, col);
                    break;
                default:
                    continue;
            }
        }
    }
}
