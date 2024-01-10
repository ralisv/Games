import argparse

from Game.board import print_hello


def main():
    # Create the parser
    parser = argparse.ArgumentParser(
        description="Accepts a dimension as a command line argument."
    )

    # Add the arguments with a default value of 10
    parser.add_argument(
        "--dimension",
        type=int,
        default=5,
        help="The dimension to be processed (positive integer).",
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Ensure the dimension is positive
    if args.dimension <= 0:
        raise ValueError("Dimension must be a positive integer.")

    # Print the dimension
    print(f"The dimension provided is: {args.dimension}")
    print_hello()


if __name__ == "__main__":
    main()
