using System;


class Program
{
    static void Main()
    {
        Game game = new Game(5, 5);
        Console.WriteLine(UI.Game(game));
    }
}
