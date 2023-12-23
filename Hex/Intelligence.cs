using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

public class Agent
{
    PlayerId playerId;

    class Node
    {
        public (int, int) move;
        public List<Node>? Children;
        public Node? parent;

        public int visitCount = 0;
        public int winCount = 0;

        public Node(Node? parent, (int, int) move)
        {
            this.parent = parent;
            this.move = move;
        }
    }

    readonly Game game;

    Node? root;

    public Agent(Game game)
    {
        this.game = game;
        this.playerId = game.CurrentPlayer == PlayerId.One ? PlayerId.Two : PlayerId.One;
    }

    static Node BestChild(Node node)
    {
        return node.Children!.Aggregate((best, next) => UTC(best) > UTC(next) ? best : next);
    }

    void Iterate(Node node)
    {
        // Selection
        while (node.Children != null)
        {
            // Debug($"Selected node {node.move} with UTC {UTC(node)} visited {node.visitCount} times and won {node.winCount} times");
            node = BestChild(node);

            (int row, int col) = node.move;
            game.Play(row, col);
        }

        PlayerId winner;
        if (!game.IsOver)
        {
            // Expansion
            if (node.visitCount > 0 && node.Children == null)
            {
                Expand(node);
                node = node.Children!.First();

                (int row, int col) = node.move;
                game.Play(row, col);
            }

            // Simulation
            winner = Simulate();
        }
        else
        {
            winner = game.CurrentPlayer;
        }
        int hasWon = winner == playerId ? 1 : 0;

        node.visitCount++;
        node.winCount += hasWon;

        // Backpropagation
        while (node.parent != null)
        {
            game.Undo();
            node = node.parent;
            node.visitCount++;
            node.winCount += hasWon;
        }
    }

    static double UTC(Node node)
    {
        if (node.visitCount == 0)
        {
            return int.MaxValue;
        }
        return (double)node.winCount / node.visitCount + 2 * Math.Sqrt(Math.Log(node.parent!.visitCount) / node.visitCount);
    }

    void Expand(Node node)
    {
        if (node.Children != null)
        {
            throw new Exception("Node already expanded");
        }
        node.Children = game.PossibleMoves().Select(move => new Node(node, move)).ToList();
    }

    PlayerId Simulate()
    {
        int depth = 0;
        while (!game.IsOver)
        {
            (int row, int col) = game.RandomPossibleMove() ?? throw new Exception("No possible moves but the game is not over.");
            game.Play(row, col);
            depth++;
        }
        // Console.WriteLine($"Won {game.CurrentPlayer == playerId}");
        // Console.WriteLine(UI.Game(game, -1, -1));
        // Thread.Sleep(10);
        var winner = game.CurrentPlayer;
        for (int i = 0; i < depth; i++)
        {
            game.Undo();
        }
        return winner;
    }

    /// <summary>
    /// Returns the best possible move for bot to make.
    /// </summary>
    public (int, int) GetMove(Game game)
    {
        root = new Node(null, (-1, -1));
        Expand(root);
        DateTime untilThen = DateTime.Now + TimeSpan.FromSeconds(0.5);
        int iterations = 0;
        while (DateTime.Now < untilThen)
        {
            Iterate(root);
            iterations++;
        }

        Console.WriteLine($"Root node visited {root.visitCount} times and won {root.winCount} times");
        return root.Children!.Aggregate((best, next) => next.visitCount > best.visitCount ? next : best).move;
    }
}