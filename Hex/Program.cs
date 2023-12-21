using System;


class Program
{
    static void Main()
    {
        var game = new Game(5, 5);
        while (true)
        {
            Console.WriteLine(UI.Game(game));
            Console.WriteLine($"Player {UI.Player(game.CurrentPlayer)}'s turn");
            Console.WriteLine("Enter row and column to play (e.g. 0 0)");
            var input = Console.ReadLine();
            if (input == "q")
            {
                break;
            }
            var parts = input.Split(' ');
            if (parts.Length != 2)
            {
                Console.WriteLine("Invalid input");
                continue;
            }
            if (!int.TryParse(parts[0], out int row) || !int.TryParse(parts[1], out int col))
            {
                Console.WriteLine("Invalid input");
                continue;
            }
            if (!game.Play(row, col))
            {
                Console.WriteLine("Invalid move");
                continue;
            }
            if (/* game.IsGameOver() */ false)
            {
                Console.WriteLine(UI.Game(game));
                Console.WriteLine($"Player {UI.Player(game.CurrentPlayer)} wins!");
                break;
            }
            Console.Clear();
        }
    }
}
