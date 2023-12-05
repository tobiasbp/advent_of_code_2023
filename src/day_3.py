#!/usr/bin/env python3
import re

from math import prod
from pathlib import Path

class Schematic:

    def __init__(self, file_path):
        """
        """

        raw_data = Path(file_path).read_text().splitlines()

        # Create a set of coordinates for all symbols in the schematic.
        # Top right position is (0, 0).
        self._symbols = []
        for line_no, l in enumerate(raw_data):
            for char_no, c in enumerate(l):
                if c not in "0123456789.":
                    s = { "pos": (char_no, line_no), "type": c}
                    self._symbols.append(s)

        # Create a list of dictionaries representing potential part
        # numbers in the schematic. Each entry has a keys
        # "top_left", "lower_right", and "value". The first two are
        # tuples of coordinates, the last is an integer.
        # the"top_left" and "lower_right" coordinates describe the square
        # around the potential part number. If a symbol exists whithin
        # this square, it is a part number.
        self._potential_parts = []
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
                self._potential_parts.append(n)

        # Create a list of parts in the schematic by
        # finding all parts that are adjacent to a symbol
        self._parts = []
        for s in self._symbols:
            self._parts += self._get_adjacent(s)

        # Create a list of gears in the schematic by
        # finding all pair of parts that are adjacent
        # to the same symbol of type "*"
        self._gears = []
        for s in [ s for s in self._symbols if s["type"] == "*" ]:
            if len(a := self._get_adjacent(s)) == 2:
                self._gears.append(a)

    def _get_adjacent(self, symbol):
        """"
        Return a list of parts which have the symbol in their square.
        """
        parts = []
        for p in self._potential_parts:
            if p["top_left"][0] <= symbol["pos"][0] <= p["lower_right"][0] and p["top_left"][1] <= symbol["pos"][1] <= p["lower_right"][1]:
                parts.append(p)
        return parts

    @property
    def part_numbers(self):
        """
        Return a list of the part numbers in the schematic.
        """
        return [ p["value"] for p in self._parts ]

    @property
    def gears(self):
        """
        Return a list of gear sizes for all pair of gears in the schematic.
        """
        r = []
        for g in self._gears:
            assert len(g) == 2, "Gear has more than two parts."
            r.append([p["value"] for p in g])
        return r


s = Schematic('data/day_3_example.txt')
answer_3_1_example = sum(s.part_numbers)
assert answer_3_1_example == 4361
print("Sum of part numbers (example):", answer_3_1_example)

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