#!/usr/bin/env python3
import re

from math import prod
from pathlib import Path

class Cards:
    """
    A collection of scratchcards.
    """

    def __init__(self, file_path):
        """
        """

        raw_data = Path(file_path).read_text().splitlines()

        # A list of dictionaries representing the cards
        self._cards = []

        for l in raw_data:
            # Get the two lists of integers
            n1, n2 = l.split(":")[-1].split("|")
            c = {}
            c["winning_numbers"] = set( int(n) for n in n1.split() )
            c["numbers_on_card"] = set( int(n) for n in n2.split() )
            c["name"] = l.split(":")[0]
            c["matching_numbers"] = c["winning_numbers"].intersection(c["numbers_on_card"])
            self._cards.append(c)

    def play(self):
        """
        Play the game according to the day 4 part 2 rules.
        Return a list of the resulting cards.
        """
        # Add a list of price cards to each card in the original collection
        # Price cards are guaranteed to never be out of range.
        for i, c in enumerate(self._cards):
            c["price_cards"] = self._cards[i+1:i+len(c["matching_numbers"])+1]

        # Copy the original cards to a new list to
        # which we will add price cards to as we go
        cards = self._cards.copy()

        i = 0
        while i < len(cards):
                cards.extend(cards[i]["price_cards"])
                i += 1

        # The deck of cards after all price cards have been added
        return cards

    @property
    def worth(self):
        """
        Return the total worth of all cards in the collection.
        This is how the answer is calculated for part 1 of day 4.
        """
        # A list of non-zero points for each card
        points = []
        for c in self._cards:
            if n := c["matching_numbers"]:
                points.append(2 ** (len(n)-1))

        # The worth of the collection is the sum of the points for the cards
        return sum(points)


c = Cards('data/day_4_example.txt')
assert c.worth == 13
print("Worth (example):", c.worth)

assert len(c.play()) == 30
print("Number of cards after play (example):", len(c.play()))



c = Cards('data/day_4.txt')
assert c.worth == 22674
print("Worth:", c.worth)

assert len(c.play()) == 5747443
print("Number of cards after play:", len(c.play()))