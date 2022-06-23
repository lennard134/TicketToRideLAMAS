# packages
import argparse

from src.model.TicketToRide import TicketToRide

INPUT_FILE = 'input'
OUTPUT_FILE = 'output'
DO = 'do'
DO_OPTIONS = []


def main():
    game = TicketToRide()
    # game.play()

    visualizer = Visualizer(game)
    visualizer.run()


def parse_args(parser) -> dict:
    args = parser.parse_args()
    return_dict = {INPUT_FILE: args.input,
                   OUTPUT_FILE: args.output,
                   DO: args.do}
    return return_dict


def make_parser():
    parser = argparse.ArgumentParser(description='Ticket to Ride')
    parser.add_argument(f"--{DO}", help=f"Do options are: {DO_OPTIONS}", default=None)
    return parser


if __name__ == "__main__":
    main()
