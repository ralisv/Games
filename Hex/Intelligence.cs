using System;
using System.Collections.Generic;
using System.Linq;

public static class Agent
{
    public static (int, int) GetMove(Game game)
    {
        Random random = new Random();
        return (random.Next(0, game.width), random.Next(0, game.height));
    }

    /// <summary>
    /// Returns sequence of coordinates from the cursor to the given coordinates, the adjacent elements
    /// differ in only one coordinate by only one point in total.
    /// </summary>
    /// <param name="cursorCol"></param>
    /// <param name="cursorRow"></param>
    /// <param name="destCol"></param>
    /// <param name="row"></param>
    /// <returns></returns>
    public static List<(int, int)> PathFromCursor((int, int) cursor, (int, int) destination)
    {
        (int cursorRow, int cursorCol) = cursor;
        (int destRow, int destCol) = destination;
        List<(int, int)> path = new() { (cursorRow, cursorCol) };

        while (cursorCol != destCol || cursorRow != destRow)
        {
            (int colDelta, int rowDelta) = (destCol - cursorCol, destRow - cursorRow);
            if (Math.Abs(colDelta) >= Math.Abs(rowDelta))
            {
                cursorCol += Math.Sign(colDelta);
            }
            else
            {
                cursorRow += Math.Sign(rowDelta);
            }
            path.Add((cursorRow, cursorCol));
        }
        return path;
    }
}