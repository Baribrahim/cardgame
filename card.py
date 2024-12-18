# card.py

class Card:
    def __init__(self, suit, rank, image_path=None):
        self.suit = suit
        self.rank = rank
        self.image = image_path  # Path to the card image

    def __str__(self):
        if self.suit == 'Joker':
            return self.rank  # e.g., 'Black Joker' or 'Red Joker'
        else:
            return f"{self.rank} of {self.suit}"

    def get_image(self):
        return self.image
