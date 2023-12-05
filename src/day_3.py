#!/usr/bin/env python3
import re

from pathlib import Path

class Schematic:

    def __init__(self, file_path):
        """
        """

        raw_data = Path(file_path).read_text().splitlines()

        # Create a set of coordinates for all symbols in the schematic.
        # Top right position is (0, 0).
        self._symbol_positions = ()
        for line_no, l in enumerate(raw_data):
            for char_no, c in enumerate(l):
                if c not in "0123456789.":
                    self._symbol_positions += ((char_no, line_no),)

        #print("Symbols:", self._symbol_positions)

        # Create a list of dictionaries representing potential part
        # numbers in the schematic. Each entry has a keys
        # "top_left", "lower_right", and "value". The first two are
        # tuples of coordinates, the last is an integer.
        # the"top_left" and "lower_right" coordinates describe the square
        # around the potential part number. If a symbol exists whithin
        # this square, it is a part number.
        potential_parts = []
        for line_no, l in enumerate(raw_data):
            #print(l)
            for match in re.finditer(r'\d+', l):
                # A potential part number and it's square
                n = {
                    "top_left": (max(0,match.span()[0]-1),max(0,line_no-1)),
                    "lower_right": (min(len(l)+1,match.span()[1]), min(len(raw_data)-1, line_no+1)),
                    "value":  int(match.group()),
                }
                # Add the potential part number to the list
                potential_parts.append(n)

        #print("Potential parts:", [p["value"] for p in potential_parts])

        # Create a list of part numbers in the schematic by checking
        # if there is a symbol within the square around the potential
        # part number.
        self._parts = []
        for pp in potential_parts:
            # Check if there is a symbol within the square
            for symbol_pos in self._symbol_positions:
                if pp["top_left"][0] <= symbol_pos[0] <= pp["lower_right"][0] and pp["top_left"][1] <= symbol_pos[1] <= pp["lower_right"][1]:
                    # If so, add the part number to the list
                    self._parts.append(pp)
                    break
        
    @property
    def parts(self):
        """
        Return a list of the part numbers in the schematic.
        """
        return [ p["value"] for p in self._parts ]

s = Schematic('data/day_3_example.txt')
answer_3_1_example = sum(s.parts)
assert answer_3_1_example == 4361
print("Sum of part numbers (example):", answer_3_1_example)

s = Schematic('data/day_3.txt')
answer_3_1 = sum(s.parts)
#assert answer_3_1 == 4361
print("Sum of part numbers:", answer_3_1)


"""
answer_2_1 = sum(d.get_possible_games(red=12, green=13, blue=14))
assert answer_2_1 == 2810
print("Sum of playable game IDs:", answer_2_1)

answer_2_2 = sum(d.get_needed_dice_products())
assert answer_2_2 == 69110
print("Sum of dice products:", answer_2_2)
"""