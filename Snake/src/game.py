import sys, os
from blessed import Terminal
from math import log
import argparse
import json
from datetime import datetime


sys.path.append(os.path.join(os.path.abspath(__file__)))

from constants import DIRECTIONS
from maps import MAPS              
from board import *


DIRECTIONS = {"KEY_UP": DIRECTIONS.UP, "KEY_DOWN": DIRECTIONS.DOWN, "KEY_LEFT": DIRECTIONS.LEFT, "KEY_RIGHT": DIRECTIONS.RIGHT}

HIGH_SCORES_FILE = os.path.expanduser("~/.snake-highscores.json")


# Helper function to update leaderboard
def update_leaderboard(map_id, score):
    filename = HIGH_SCORES_FILE
    new_highscore = False
    map_id = map_id

    try:
        # Load existing leaderboard
        with open(filename, 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty/invalid, start a new leaderboard
        leaderboard = {}

    new_record = {"score": score, "date": datetime.now().strftime("%Y-%m-%d %H:%M")}

    # Update the leaderboards for this map
    if map_id not in leaderboard or len(leaderboard[map_id]) < 3:
        leaderboard.setdefault(map_id, []).append(new_record)
        new_highscore = True
    else:
        # Check if this score beats a previous record
        if score > min(record['score'] for record in leaderboard[map_id]):
            # Remove the lowest score
            leaderboard[map_id].remove(min(leaderboard[map_id], key=lambda record: record['score']))

            # Add the new high score
            leaderboard[map_id].append(new_record)
            new_highscore = True

    # Ensure leaderboard for this map only keeps top 3 scores
    leaderboard[map_id] = sorted(leaderboard[map_id], key=lambda record: -record['score'])

    # Save updated leaderboard
    with open(filename, 'w') as f:
        json.dump(leaderboard, f)

    # If a new high score has been achieved, print a message
    if new_highscore:
        print(f"\nCongrats! You achieved a new high score of {score} on map {map_id}!")

    # Print the top three scores for the map
    print(f"\nTop 3 scores for map {map_id}:")
    for i, record in enumerate(leaderboard[map_id], start=1):
        print(f"{i}) Score: {record['score']}, Date: {record['date']}")


def main():
    parser = argparse.ArgumentParser(description = "CLI implementation of the Snake game")

    parser.add_argument("--map", type = str, default = "plain", help = "Map to play on")
    parser.add_argument("--fruits", type = int, default = 0, help = "Number of fruits to eat before winning")

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
            inp = term.inkey(timeout = max(0.15, (1 - log(len(board.snake), 100)) / snake_map.speed))  # Snake moves every half second
            if inp.name in DIRECTIONS:
                board.set_direction(DIRECTIONS[inp.name])

            # Move the snake
            if not board.move_snake():
                break  # Game over

    print(term.normal)
    print(f"Game over! Your final score was {len(board.snake)}")

    # Update leaderboard
    update_leaderboard(args.map, len(board.snake))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(2)