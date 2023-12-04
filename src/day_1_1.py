#!/usr/bin/env python3
from pathlib import Path

data = Path('data/day_1.txt').read_text().splitlines()

answer = 0

for l in data:
    # A list of all digits chars in the line
    n = [ c for c in l if c.isdigit()]

    # Concatinate diigits and add the value to the answer
    answer += int(n[0] + n[-1])  

print("Day 1,1: ", answer)