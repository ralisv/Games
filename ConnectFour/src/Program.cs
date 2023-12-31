﻿using System;
using System.Threading;


class Program
{
    static void EndGame(Game game, string message)
    {
        Console.Clear();
        Console.WriteLine(UI.Game(game, -1));
        Console.WriteLine(message);
    }

    static void HumanPlay(Game game, ref int currentCol)
    {
        Console.Clear();
        Console.WriteLine(UI.Game(game, currentCol));
        Console.WriteLine("Use arrow keys to choose a column. Press space to play. Press 'q' to quit.");

        var keyInfo = Console.ReadKey(true);
        switch (keyInfo.Key)
        {
            case ConsoleKey.LeftArrow:
                currentCol = Math.Max(0, currentCol - 1);
                break;
            case ConsoleKey.RightArrow:
                currentCol = Math.Min(game.Width - 1, currentCol + 1);
                break;
            case ConsoleKey.Spacebar:
                PlayResult result = game.Play(currentCol);
                if (result == PlayResult.Again)
                {
                    Console.WriteLine("That column is full. Try again.");
                }
                else if (result == PlayResult.Draw)
                {
                    EndGame(game, "It's a draw!");
                    Environment.Exit(0);
                }
                else if (result == PlayResult.Win)
                {
                    EndGame(game, $"Player {UI.Player(game.CurrentPlayer)} wins!");
                    Environment.Exit(0);
                }
                Console.Clear();
                Console.WriteLine(UI.Game(game, currentCol));
                break;
            case ConsoleKey.Q:
                Environment.Exit(0);
                break;
        }
    }

    static void BotPlay(Game game, ref int currentCol)
    {
        Thread.Sleep(250);
        int col = Agent.GetMove(game);

        // Determine the direction of movement
        int step = col > currentCol ? 1 : -1;

        // Move towards the target column with visual feedback
        while (currentCol != col)
        {
            Console.Clear();
            Console.WriteLine(UI.Game(game, currentCol));
            Thread.Sleep(300);
            currentCol += step;
        }

        Console.Clear();
        Console.WriteLine(UI.Game(game, currentCol));
        Thread.Sleep(300);

        PlayResult result = game.Play(col);
        if (result == PlayResult.Draw)
        {
            EndGame(game, "It's a draw!");
            Environment.Exit(0);
        }
        else if (result == PlayResult.Win)
        {
            EndGame(game, $"Player {UI.Player(game.CurrentPlayer)} wins!");
            Environment.Exit(0);
        }
    }

    static int Main(string[] args)
    {
        bool bot = args.Length != 0 && args[0] == "bot";

        Game game = new Game(8, 8, PlayerSymbol.X, 4);
        int currentCol = 0;

        while (true)
        {
            if (bot && game.CurrentPlayer == PlayerSymbol.O)
            {
                BotPlay(game, ref currentCol);
            }
            else
            {
                HumanPlay(game, ref currentCol);
            }
        }
    }
}
