#!/usr/bin/env python3
from pathlib import Path

data = Path('data/day_1.txt').read_text().splitlines()

# The position + 1 is the numeric value of the strings
string_to_digit = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

answer = 0

def string_digit_to_int(line):

    # Find all occurences of digit strings    
    # Keys in dict are positions of match in line. Values are the digit strings
    x = {}
    for s in string_to_digit:
        for i in range(len(line)):
            if line[i:].startswith(s):
                x[i] = s
    
    # No matches found
    if len(x) == 0:
        return line

    # Get higest and lowest position of match    
    i_min = min(x.keys())
    i_max = max(x.keys())

    # Swap the first char of first and last string digit with numeric value
    line = line[:i_min] + str(string_to_digit.index(x[i_min]) + 1) + line[i_min + 1:]
    line = line[:i_max] + str(string_to_digit.index(x[i_max]) + 1) + line[i_max + 1:]

    # The modified line
    return line


def first_last_digits_to_int(line):
    # A list of all digits chars in the line
    n = [ c for c in line if c.isdigit()]

    assert len(n) > 0, f"Line must have at least a single digit: '{line}'"

    # Concatinate first and last digit (could be the same positon) as an int    
    return int(n[0] + n[-1])


for i, l in enumerate(data):
    print("Original:", l)
    l = string_digit_to_int(l)
    print("String to int:", l)
    value = first_last_digits_to_int(l)
    print(f"Line {i}:", value)
    answer += value
    print()

print("Day 1,2: ", answer)

assert answer == 54728, f"Wrong answer for day 1,2: {answer}"
