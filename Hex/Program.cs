using System;
using System.Threading;

class Program
{
    static int Main()
    {
        int cursorRow = 0;
        int cursorCol = 0;
        var game = new Game(7, 7);
        while (true)
        {   
            string precalculatedBoard = UI.Game(game, cursorRow, cursorCol);
            Console.Clear();
            Console.WriteLine(precalculatedBoard);

            if (game.IsOver)
            {
                Console.WriteLine($"Player {UI.Player(game.CurrentPlayer)} wins!");
                return 0;
            }

            if (game.CurrentPlayer == PlayerId.Two) {
                (int destRow, int destCol) = Agent.GetMove(game);
                foreach ((int, int) coord in Agent.PathFromCursor(cursorRow, cursorCol, destRow, destCol))
                {
                    cursorRow = coord.Item1;
                    cursorCol = coord.Item2;
                    Thread.Sleep(200);
                    precalculatedBoard = UI.Game(game, cursorRow, cursorCol);
                    Console.Clear();
                    Console.WriteLine(precalculatedBoard);
                }
                game.Play(cursorRow, cursorCol);
                continue;
            }

            switch (Console.ReadKey().Key) {
                case ConsoleKey.Q:
                    return 0;
                case ConsoleKey.UpArrow:
                    cursorRow = Math.Max(0, cursorRow - 1);
                    break;
                case ConsoleKey.DownArrow:
                    cursorRow = Math.Min(game.height - 1, cursorRow + 1);
                    break;
                case ConsoleKey.LeftArrow:
                    cursorCol = Math.Max(0, cursorCol - 1);
                    break;
                case ConsoleKey.RightArrow:
                    cursorCol = Math.Min(game.width - 1, cursorCol + 1);
                    break;
                case ConsoleKey.Spacebar:
                    game.Play(cursorRow, cursorCol);
                    break;
                default:
                    continue;
            }
        }
    }
}
