using System;
using System.Collections.Generic;
using System.Linq;


static class Util
{
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
        path.Add(destination);
        return path;
    }

    public static bool InCorner((int, int) hexCoords, int width, int height)
    {
        var (row, col) = hexCoords;
        return (row == 0 && col == 0) ||
            (row == 0 && col == width - 1) ||
            (row == height - 1 && col == 0) ||
            (row == height - 1 && col == width - 1);
    }

    public static bool IsAdjacentToCursor(int cursorRow, int cursorCol, int row, int col)
    {
        int colDelta = cursorCol - col;
        int rowDelta = cursorRow - row;
        return Hexagon.AdjacentCoords.Contains((rowDelta, colDelta));
    }
}