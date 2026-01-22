#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY shots
#  2. 2D_INTEGER_ARRAY players
#

def solve(shots, players):
    # Write your code here
    from bisect import bisect_right, bisect_left

    starts = sorted(a for a, b in shots)
    ends = sorted(b for a, b in shots)

    total = 0
    for c, d in players:
        total += bisect_right(starts, d) - bisect_left(ends, c)  # a<=d minus b<c
    return total

    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    shots = []

    for _ in range(n):
        shots.append(list(map(int, input().rstrip().split())))

    players = []

    for _ in range(m):
        players.append(list(map(int, input().rstrip().split())))

    result = solve(shots, players)

    fptr.write(str(result) + '\n')

    fptr.close()
