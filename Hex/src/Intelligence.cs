using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

public class Agent
{
    PlayerId playerId;

    /// <summary>
    /// Time in milliseconds to wait for the agent to make a move.
    /// </summary>
    readonly int waitTime;

    /// <summary>
    /// Represents a node in the Monte Carlo tree.
    /// </summary>
    class Node
    {
        /// <summary>
        /// The move that led to this node.
        /// </summary>
        public (int, int) move;

        /// <summary>
        /// List of children of this node.
        /// </summary>
        public List<Node>? Children;

        /// <summary>
        /// Parent of this node.
        /// </summary>
        public Node? parent;

        /// <summary>
        /// Number of times this node was visited.
        /// </summary>
        public int visitCount = 0;

        /// <summary>
        /// Number of times this node was visited and the game was won by the bot.
        /// </summary>
        public int winCount = 0;
        
        public Node(Node? parent, (int, int) move)
        {
            this.parent = parent;
            this.move = move;
        }
    }

    /// <summary>
    /// The instance of the game that the agent is playing.
    /// </summary>
    readonly Game game;

    /// <summary>
    /// The root node of the Monte Carlo tree.
    /// </summary>
    Node? root;

    /// <summary>
    /// Creates a new agent that plays the given game.
    /// </summary>
    /// <param name="game"></param>
    /// <param name="waitTime"></param>
    public Agent(Game game, int waitTime)
    {
        this.game = game;
        this.playerId = game.CurrentPlayer;
        this.waitTime = waitTime;
    }

    /// <summary>
    /// Returns the best child of the given node according to the UCT algorithm.
    /// </summary>
    /// <param name="node"></param>
    /// <returns> Node with the highest UCT score </returns>
    static Node BestChild(Node node)
    {
        return node.Children!.Aggregate((best, next) => UTC(best) > UTC(next) ? best : next);
    }

    /// <summary>
    /// Performs one iteration of the Monte Carlo tree search. This consists of four steps:
    /// 1. Selection
    /// 2. Expansion
    /// 3. Simulation
    /// 4. Backpropagation
    /// 
    /// Beware, due to optimizations, this method mutates the game state and relies on the perfectly
    /// correct implementation of the Game.Undo method. Thanks to that, it is never necessary to
    /// create a copy of the game state.
    /// </summary>
    /// <param name="root"></param>
    void Iterate()
    {
        // Recursively browses the tree and selects the best leaf node.
        while (root!.Children != null)
        {
            root = BestChild(root);

            (int row, int col) = root.move;
            game.Play(row, col);
        }

        PlayerId winner;
        if (!game.IsOver)
        {
            // Expansion
            if (root.visitCount > 0 && root.Children == null)
            {
                Expand(root);
                root = root.Children!.First();

                (int row, int col) = root.move;
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

        root.visitCount++;
        root.winCount += hasWon;

        // Backpropagation
        while (root.parent != null)
        {
            game.Undo();
            root = root.parent;
            root.visitCount++;
            root.winCount += hasWon;
        }
    }

    /// <summary>
    /// Returns the UCT score of the given node.
    /// </summary>
    /// <param name="node"></param>
    /// <returns> Double, the higher the value, the more interesting this node is to the MCTS </returns>
    static double UTC(Node node)
    {
        if (node.visitCount == 0)
        {
            return int.MaxValue;
        }
        return (double)node.winCount / node.visitCount + 2 * Math.Sqrt(Math.Log(node.parent!.visitCount) / node.visitCount);
    }

    /// <summary>
    /// Expands the given node by creating a child node for each possible move.
    /// </summary>
    /// <param name="node"></param>
    /// <exception cref="Exception"></exception>
    void Expand(Node node)
    {
        if (node.Children != null)
        {
            throw new Exception("Node already expanded");
        }
        node.Children = game.PossibleMoves().Select(move => new Node(node, move)).ToList();
    }

    /// <summary>
    /// Performs a random simulation of the game until it is over and returns the winner.
    /// </summary>
    /// <returns> The winner of the simulation </returns>
    /// <exception cref="Exception"></exception>
    PlayerId Simulate()
    {
        int depth = 0;
        while (!game.IsOver)
        {
            (int row, int col) = game.RandomPossibleMove() ?? throw new Exception("No possible moves but the game is not over.");
            game.Play(row, col);
            depth++;
        }

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
    public (int, int) GetMove()
    {
        // Create and expand the root node initially
        root = new Node(null, (-1, -1));
        Expand(root);

        // Run the Monte Carlo tree search for the given amount of time
        DateTime untilThen = DateTime.Now + TimeSpan.FromMilliseconds(waitTime);
        int iterations = 0;
        while (DateTime.Now < untilThen)
        {
            Iterate();
            iterations++;
        }

        // Print some statistics
        Console.WriteLine($"Root node visited {root.visitCount} times and won {root.winCount} times");

        // Return the most visited child of the root node
        return root.Children!.Aggregate((best, next) => next.visitCount > best.visitCount ? next : best).move;
    }
}
