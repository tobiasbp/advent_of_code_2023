#!/usr/bin/env python3
import re

from math import prod, inf
from pathlib import Path

class Almanac:
    """
    An almanac of seeds and various translation maps.
    """

    def __init__(self, file_path):
        """
        """

        raw_data = Path(file_path).read_text().splitlines()

        # Parse the list of seed integers on the first line

        # Parsing as decribed in problem part one
        self._seeds_v1 = [int(n) for n in raw_data[0].split(':')[-1].split()]
        # Parsing as decribed in problem part two
        #for x, y in :
        #    print(x, y)

        self._maps = {}
        current_map_name = None

        # Parse the maps beginning in line 3
        for l in raw_data[2:]:
            if data := (l.split()):
                if data[-1] == "map:":
                    # Add a new map entry
                    current_map_name = data[0]
                    self._maps[current_map_name] = {"ranges": []}
                else:
                    # Add a range to the current map
                    self._maps[current_map_name]["ranges"].append([int(n) for n in data])
    
    def _map(self, map_name:str, value:int):
        for r in self._maps[map_name]["ranges"]:
            if r[1] <= value <= r[1]+r[2]-1:
                d = r[0] - r[1]
                return value + d
        
        # If the value is in no range, there is no change in the mapping
        return value

    # Dedicated methods for beauty
    def seed_to_soil(self, s:int):
        return self._map("seed-to-soil", s)

    def soil_to_fertilizer(self, s:int):
        return self._map("soil-to-fertilizer", s)

    def fertilizer_to_water(self, f:int):
        return self._map("fertilizer-to-water", f)

    def water_to_light(self, w:int):
        return self._map("water-to-light", w)

    def light_to_temperature(self, l:int):
        return self._map("light-to-temperature", l)

    def temperature_to_humidity(self, t:int):
        return self._map("temperature-to-humidity", t)

    def humidity_to_location(self, h:int):
        return self._map("humidity-to-location", h)
    
    def seed_to_location(self, s:int):
        r = self.seed_to_soil(s)
        r = self.soil_to_fertilizer(r)
        r = self.fertilizer_to_water(r)
        r = self.water_to_light(r)
        r = self.light_to_temperature(r)
        r = self.temperature_to_humidity(r)
        r = self.humidity_to_location(r)
        return r

    @property
    def seeds_v1(self):
        """
        Seeds according to problem part one.
        """
        return self._seeds_v1

    @property
    def seeds_v2(self):
        """
        Seeds according to problem part two.
        """
        for r in zip(self._seeds_v1[::2], self._seeds_v1[1::2]):
            for s in range(r[0], r[0]+r[1]):
                yield s



a = Almanac('data/day_5_example.txt')

assert a.seed_to_soil(0) == 0
assert a.seed_to_soil(50) == 52
assert a.seed_to_soil(98) == 50
assert a.seed_to_soil(100) == 100
assert a.seed_to_soil(79) == 81
assert a.seed_to_soil(14) == 14
assert a.seed_to_soil(55) == 57
assert a.seed_to_soil(13) == 13

assert a.seed_to_location(79) == 82
assert a.seed_to_location(14) == 43
assert a.seed_to_location(55) == 86
assert a.seed_to_location(13) == 35

a_1_e = min([a.seed_to_location(s) for s in a.seeds_v1])
assert a_1_e == 35
print("Lowest location part 1 (example):", a_1_e)

a_2_e = min([a.seed_to_location(s) for s in a.seeds_v2])
assert a_2_e == 46
print("Lowest location part 1 (example):", a_2_e)


a = Almanac('data/day_5.txt')
a_1 = min([a.seed_to_location(s) for s in a.seeds_v1])
assert a_1 == 486613012
print("Lowest location part 1:", a_1)

"""
# WARNING: This takes a long time to run. 220 minutes on my machine.
a_2 = inf
for s in a.seeds_v2:
    if (l := a.seed_to_location(s)) < a_2:
        a_2 = l
        print(a_2)
 
assert a_2 == 56931769
print("Lowest location part 2:", a_2)
"""