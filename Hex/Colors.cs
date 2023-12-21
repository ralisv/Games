using System;
using System.Runtime.InteropServices;

public static class ConsoleColors
{
    public static string Bold => "\x1b[1m";
    public static string Underline => "\x1b[4m";

    public static string ForegroundColor(int red, int green, int blue) =>
        $"\x1b[38;2;{red};{green};{blue}m";

    public static string BackgroundColor(int red, int green, int blue) =>
        $"\x1b[48;2;{red};{green};{blue}m";}

public static class Color
{
    public static string Reset => "\x1b[0m";

    public static string Grey => ConsoleColors.ForegroundColor(127, 127, 127);
    public static string LightGrey => ConsoleColors.ForegroundColor(200, 200, 200);
    public static string Red => ConsoleColors.ForegroundColor(255, 0, 0);
    public static string LightRed => ConsoleColors.ForegroundColor(255, 127, 127);
    public static string Blue => ConsoleColors.ForegroundColor(0, 127, 255);
    public static string LightBlue => ConsoleColors.ForegroundColor(50, 180, 255);
}
