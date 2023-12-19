using System.Collections.Generic;


static class UI { }


class Game
{
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
}