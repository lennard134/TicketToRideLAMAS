# packages
import argparse

from model.TicketToRide import TicketToRide
from Visualizer import Visualizer

NUM_AGENTS = 'n'
NUM_ROUTE_CARDS = 'm'
ALLOWED_AGENTS = [2, 3, 4, 5]
DEFAULT_NUM_AGENTS = 3
DEFAULT_NUM_ROUTE_CARDS = 2


def main():
    """
        Main function to play ticket to ride
    """
    parser = make_parser()
    arguments = parse_args(parser)

    ticket_to_ride_game = TicketToRide(num_agents=arguments[NUM_AGENTS],
                                       num_route_cards=arguments[NUM_ROUTE_CARDS])

    visualizer = Visualizer(ticket_to_ride_game)
    visualizer.run()


def parse_args(parser) -> dict:
    """
        Parses arguments from user input
    """
    print()
    args = parser.parse_args()

    try:
        num_agents = int(args.num_agents)
    except ValueError:
        print(f"INVALID NUMBER FOR NUMBER OF AGENTS. USING DEFAULT = {DEFAULT_NUM_AGENTS}.")
        num_agents = DEFAULT_NUM_AGENTS

    if num_agents not in ALLOWED_AGENTS:
        print(f"INVALID NUMBER FOR NUMBER OF AGENTS. CHOOSE IN {ALLOWED_AGENTS}. "
              f"USING DEFAULT = {DEFAULT_NUM_AGENTS}.\n")
        num_agents = DEFAULT_NUM_AGENTS

    try:
        num_route_cards = int(args.num_route_cards)
    except ValueError:
        print(f"INVALID NUMBER FOR NUMBER OF ROUTE CARDS. USING DEFAULT = {DEFAULT_NUM_ROUTE_CARDS}.")
        num_route_cards = DEFAULT_NUM_ROUTE_CARDS
        
    if num_route_cards < 1:
        print(f"INVALID NUMBER FOR NUMBER OF ROUTE CARDS. MUST BE AT LEAST 1. "
              f"USING DEFAULT = {DEFAULT_NUM_ROUTE_CARDS}.")
        num_route_cards = DEFAULT_NUM_ROUTE_CARDS

    return_dict = {NUM_AGENTS: num_agents,
                   NUM_ROUTE_CARDS: num_route_cards}
    print()
    return return_dict


def make_parser():
    """
        Makes a parser for user input
    """
    parser = argparse.ArgumentParser(description='Ticket to Ride')
    parser.add_argument(f"--num_agents", '-n', help=f"The number of agents. Options={{2,...,5}}.",
                        default=DEFAULT_NUM_AGENTS)
    parser.add_argument(f"--num_route_cards", '-m', help=f"The number of route cards per agent.",
                        default=DEFAULT_NUM_ROUTE_CARDS)
    return parser


if __name__ == "__main__":
    main()
