using System;
using System.Threading;


enum PlayerSymbol
{
    X,
    O
}


static class Intelligence
{
    readonly static PlayerSymbol BotPlayer = PlayerSymbol.O;

    public static int GetMove(Game game)
    // Select the best col based on output of MiniMax
    {
        MiniMax(game, int.MinValue, int.MaxValue, 5, out int bestCol);
        return bestCol;
    }

    public static int Evaluate(Game game)
    {
        if (game.Finished)
        {
            if (game.IsDraw())
            {
                return -1;
            }
            else if (game.CurrentPlayer == BotPlayer)
            {
                return 100;
            }
            else
            {
                return -100;
            }
        }
        else
        {
            return 0;
        }
    }

    public static int MiniMax(Game game, int alfa, int beta, int depth, out int bestCol)
    {
        bestCol = 0;

        if (depth == 0 || game.Finished || game.IsDraw())
        {
            return Evaluate(game);
        }


        if (game.CurrentPlayer == BotPlayer)
        {
            // Maximizing player
            for (int col = 0; col < game.Width; col++)
            {
                if (game.Board[0][col] != null)
                {
                    continue;
                }

                game.Play(col);
                int value = MiniMax(game, alfa, beta, depth - 1, out int _);

                if (value > alfa)
                {
                    alfa = value;
                    bestCol = col;
                }

                game.Undo();

                if (beta <= alfa)
                {
                    break;
                }
            }
            return alfa;
        }
        else
        {
            // Minimizing player
            for (int col = 0; col < game.Width; col++)
            {
                if (game.Board[0][col] != null)
                {
                    continue;
                }

                game.Play(col);
                int value = MiniMax(game, alfa, beta, depth - 1, out int _);

                if (value < beta)
                {
                    beta = value;
                    bestCol = col;
                }

                game.Undo();

                if (beta <= alfa)
                {
                    break;
                }

            }
            return beta;
        }
    }
}