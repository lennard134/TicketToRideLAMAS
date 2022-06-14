"""
This class represents the deck of playing cards with coloured wagons and locomotives
"""
import random

NR_COLOUR_CARDS = 12
NR_TRAINS = 14
TRAIN_COLOURS = [
    'red', 'pink', 'white', 'yellow', 'green', 'blue', 'black', 'orange', 'joker'
]


class Deck(object):
    def __init__(self):
        self.closed_cards = []
        self.open_cards = []  # 5 open cards
        self.used_cards = []

        self._init_cards()

    def _init_cards(self):
        """
        function to initialize a new deck of playing cards
        """
        deck = []
        for colour in TRAIN_COLOURS:
            if not colour == "joker":
                deck.extend(NR_COLOUR_CARDS * [colour])
            else:
                deck.extend(NR_TRAINS * [colour])
        random.shuffle(deck)
        self.closed_cards = deck

    def remove_open_card(self, colour: str):
        """
        Remove a card from the open deck
        """
        assert colour in self.open_cards, "COLOUR NOT IN OPEN CARD"

        self.open_cards.remove(colour)
        self.open_cards.append(self.remove_closed_card())

    def remove_closed_card(self):
        """
        Remove a card from the closed deck
        """
        return self.closed_cards.pop()

    def shuffle_used_cards(self):
        """
        Gets called if closed card deck is empty and shuffles the played cards
        """
        self.closed_cards.extend(self.used_cards)
        random.shuffle(self.closed_cards)


if __name__ == "__main__":
    Deck()
