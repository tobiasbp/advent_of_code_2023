#!/usr/bin/env python3
from pathlib import Path

class GameData:

    def __init__(self, file_path):
        """
        Parse the data file to a list of games with a
        list of samples as dictionaries with colors as keys.
        [{'red': 1, 'blue': 2}, {'red': 2, 'blue': 1}]
        """
        raw_data = Path(file_path).read_text().splitlines()

        self._game_data = []

        for l in raw_data:
            sample_sets = []
            for samples in l.split(':')[-1].strip().split(';'):
                sample_sets.append(
                    { s.strip().split(" ")[-1]:int(s.strip().split(" ")[0]) for s in samples.split(",")}
                    )

            self._game_data.append(sample_sets)

    @property
    def game_data(self):
        return self._game_data        

    def get_games_max(self, red:int, green:int, blue:int):
        """
        Get a list of ids for games that could have been played if the
        bag contained the argument number of cubes of each color
        """
        game_ids = []

        for i, game in enumerate(self.game_data, start = 1):
            print("Games:", game)
            max_cubes_seen = self.max_cubes(game)
            print("Max:", max_cubes_seen)
            print()
            if max_cubes_seen.get('red', 0) <= red and max_cubes_seen.get('green', 0)  <= green and max_cubes_seen.get('blue', 0) <= blue:
                game_ids.append(i)

        return game_ids

    def max_cubes(self, game):
        """
        Get the maximum number of number of cubes for
        each color in a list of sample dicts
        """
        max_cubes = {}
        for sample_set in game:
            for color, samples in sample_set.items():
                if max_cubes.get(color, 0) < samples:
                    max_cubes[color] = samples

        return max_cubes

d = GameData('data/day_2.txt')

print("Sum of playable game IDs:", sum(d.get_games_max(red=12, green=13, blue=14)))

      