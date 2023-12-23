# ConnectFour Game with AI Bot
## Overview
This is a ConnectFour game implemented in C# with an AI bot opponent. The AI bot uses the minimax algorithm with alpha-beta pruning to determine its moves. The game is played in a console window and uses Unicode characters to display the game board.
## How to Play
The game is played on a grid that's 8 cells wide and 8 cells high. The players take turns putting their tokens in one of the columns. The token falls down to the lowest empty cell in the selected column. The first player to get four of their tokens in a row (horizontally, vertically, or diagonally) is the winner.
When it's your turn, use the arrow keys to choose a column and press space to play your token in that column. If you want to quit the game, press 'q'.
## AI Bot
The AI bot uses the minimax algorithm with alpha-beta pruning to determine its moves. The minimax algorithm is a recursive algorithm used for decision making in game theory and artificial intelligence. Alpha-beta pruning is an optimization technique that reduces the number of nodes evaluated by the minimax algorithm.
The AI bot evaluates the current state of the game and returns the best move for it to make.
## Code Structure
The code is divided into several classes:
Game: Represents a game of Connect Four. It contains the game board and the game logic.
Agent: Represents the AI bot. It contains the minimax algorithm and the game state evaluation function.
UI: Handles the game's user interface. It contains functions for displaying the game board and the game result.
Program: Contains the main function. It handles the game loop and the player input.
## Running the Game
To run the game, compile the C# files and run the resulting executable. If you want the AI bot to play first, pass "bot" as a command-line argument.
Contributing
Contributions are welcome. Please open an issue to discuss your ideas or submit a pull request.
