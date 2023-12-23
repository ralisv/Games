import argparse
import os
import sys
from math import log

from blessed import Terminal

sys.path.append(os.path.join(os.path.abspath(__file__)))

from board import *
from constants import DIRECTIONS
from maps import MAPS

key_to_direction_map = {
    "KEY_UP": DIRECTIONS.UP,
    "KEY_DOWN": DIRECTIONS.DOWN,
    "KEY_LEFT": DIRECTIONS.LEFT,
    "KEY_RIGHT": DIRECTIONS.RIGHT,
}


def main():
    parser = argparse.ArgumentParser(description="CLI implementation of the Snake game")

    parser.add_argument("--map", type=str, default="plain", help="Map to play on")
    parser.add_argument(
        "--fruits", type=int, default=0, help="Number of fruits to eat before winning"
    )

    args = parser.parse_args()
    snake_map = MAPS[args.map]
    snake_map.fruits = args.fruits or snake_map.fruits

    # Initialize the board
    board = Board(snake_map)

    # blessed Terminal initialization
    term = Terminal()

    with term.cbreak(), term.hidden_cursor():
        while True:
            print(term.clear + str(board))

            # Handle input
            inp = term.inkey(
                timeout=max(0.15, (1 - log(len(board.snake), 100)) / snake_map.speed)
            )  # Snake moves every half second
            if inp.name in key_to_direction_map:
                board.set_direction(key_to_direction_map[inp.name])

            # Move the snake
            if not board.move_snake():
                break  # Game over

    print(term.normal)
    print(f"Game over! Your final score was {len(board.snake)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)
