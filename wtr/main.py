"""`wtr` main entry point."""
import argparse


def main():
    """Run the `wtr` app."""
    parser = argparse.ArgumentParser(
        description="wtr is a command-line weather application. It shows the weather for the given locations."
    )
    initialize_parser(parser)
    parser.parse_args()


def initialize_parser(parser):
    """Initialize the required arguments for the `wtr` app."""
    parser.add_argument("location", help="Location to get weather for.", nargs="+")
    parser.add_argument(
        "-w", "--week", help="Show the weather for the next week starting from today.", action="store_true"
    )


if __name__ == "__main__":
    main()
