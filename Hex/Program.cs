using System;


class Program
{
    static int Main()
    {
        int row = 0;
        int col = 0;
        var game = new Game(10, 10);
        while (true)
        {
            Console.Clear();
            Console.WriteLine(UI.Game(game, row, col));
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
