# deck.py

import random
from card import Card

class Deck:
    def __init__(self, include_jokers=False):
        self.cards = []
        self.build_deck(include_jokers)

    def build_deck(self, include_jokers):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = [
            '2', '3', '4', '5', '6', '7', '8', '9', '10',
            'Jack', 'Queen', 'King', 'Ace'
        ]

        # Create the standard 52 cards
        for suit in suits:
            for rank in ranks:
                image_path = f"static/images/{rank}_of_{suit}.png"
                self.cards.append(Card(suit, rank, image_path))

        # Include Jokers if specified
        if include_jokers:
            self.cards.append(Card('Joker', 'Black Joker', 'static/images/Black_Joker.png'))
            self.cards.append(Card('Joker', 'Red Joker', 'static/images/Red_Joker.png'))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_one(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None  # Deck is empty
