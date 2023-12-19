using System.Collections.Generic;
using System;

static class UI { }


class Game
{
    public static enum PlayResult {
        Again,
        Draw,
        Win
    }

    public readonly uint Height;
    public readonly uint Width;
    private readonly List<List<Player?>> Board;

    public Player CurrentPlayer { get; private set; }

    public Game(uint height, uint width, Player? startingPlayer)
    {
        Height = height;
        Width = width;
        Board = new();

        for (int row = 0; row < Height; row++)
        {
            Board.Add(new());
            for (int col = 0; col < Width; col++)
            {
                Board[row].Add(null);
            }
        }

        CurrentPlayer = startingPlayer ?? Player.X;
    }

    public PlayResult Play(uint col) {
        if (col >= Width) {
            return PlayResult.Again;
        }

        Board[0][(int)col] = CurrentPlayer;
        CurrentPlayer = CurrentPlayer == Player.X ? Player.O : Player.X;
    }
}
