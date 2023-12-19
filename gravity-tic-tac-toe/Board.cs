using System.Collections.Generic;


static class UI { }


class Game
{
    readonly uint Height;
    readonly uint Width;

    readonly List<List<Player?>> Board;

    public Game(uint height, uint width)
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
    }
}