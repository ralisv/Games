using System;
using System.Threading;


class Program
{
    static readonly int Dimension = 12;
    static readonly int WaitTime = 1000;

    static int Main(string[] args)
    {
        bool playWithBot = args.Length > 0 && args[0] == "bot";
        int cursorRow = 0;
        int cursorCol = 0;
        var game = new Game(Dimension, Dimension);
        Agent agent = new(game, WaitTime);

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

            // Bot's turn
            if (game.CurrentPlayer == PlayerId.Two && playWithBot) {
                var move = agent.GetMove();

                var cursorMoves = Util.PathFromCursor((cursorRow, cursorCol), move);
                foreach ((int cRow, int cCol) in cursorMoves)
                {
                    cursorRow = cRow;
                    cursorCol = cCol;
                    Thread.Sleep(200);
                    precalculatedBoard = UI.Game(game, cursorRow, cursorCol);
                    Console.Clear();
                    Console.WriteLine(precalculatedBoard);
                }
                Thread.Sleep(200);
                game.Play(cursorRow, cursorCol);
                continue;
            }

            // Player's turn
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
