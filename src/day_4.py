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

        self._cards = []

        for l in raw_data:
            c = {}
            n1, n2 = l.split(":")[-1].split("|")
            c["winning_numbers"] = set( int(n) for n in n1.split() )
            c["numbers_on_card"] = set( int(n) for n in n2.split() )
            c["name"] = l.split(":")[0]
            self._cards.append(c)
 
    @property
    def worth(self):
        """
        Return the total worth of all cards in the collection.
        This is how the answer is calculated for part 1 of day 4.
        """
        # A list of points for each card
        points = []
        for c in self._cards:
            if n := c["numbers_on_card"].intersection(c["winning_numbers"]):
                points.append(2 ** (len(n)-1))
            else:
                points.append(0)
        
        # The worth of the collection is the sum of the points for the cards
        return sum(points)


c = Cards('data/day_4_example.txt')
assert c.worth == 13
print("Worth (example):", c.worth)


c = Cards('data/day_4.txt')
assert c.worth == 22674
print("Worth:", c.worth)


"""
answer_3_2_example = sum([prod(g) for g in s.gears])
assert answer_3_2_example == 467835
print("Gears (example):", answer_3_2_example)

s = Schematic('data/day_3.txt')
answer_3_1 = sum(s.part_numbers)
assert answer_3_1 == 519444
print("Sum of part numbers:", answer_3_1)

answer_3_2 = sum([prod(g) for g in s.gears])
assert answer_3_2 == 74528807
print("Gears:", answer_3_2)
"""