using System;


static class Agent
{
    readonly static Random random = new Random();
    readonly static PlayerSymbol BotPlayer = PlayerSymbol.O;

    /// <summary>
    /// Returns the best move for the bot to make.
    /// </summary>
    /// <param name="game"> Game instance, Bot should be playing </param>
    /// <returns></returns>
    public static int GetMove(Game game)
    {
        MiniMax(game, int.MinValue, int.MaxValue, 8, out int bestCol);
        return bestCol;
    }

    /// <summary>
    /// Evaluates the current state of the game.
    /// </summary>
    /// <param name="game"> Game instance </param>
    static int Evaluate(Game game)
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
            return random.Next(0, 50);
        }
    }

    /// <summary>
    /// Minimax algorithm with alpha-beta pruning.
    /// </summary>
    /// <param name="game"> Game instance </param>
    /// <param name="alfa"> Best possible value for Max node </param>
    /// <param name="beta"> Best possible value for Min node </param>
    /// <param name="depth"> Maximum depth the search can reach </param>
    /// <param name="bestCol"> Column with best results </param>
    /// <returns></returns>
    static int MiniMax(Game game, int alfa, int beta, int depth, out int bestCol)
    {
        bestCol = -1;
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