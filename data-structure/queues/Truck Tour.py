#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'truckTour' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY petrolpumps as parameter.
#

def truckTour(petrolpumps):
    # Write your code here
    start = 0
    tank = 0
    total = 0

    for i, (petrol, dist) in enumerate(petrolpumps):
        gain = petrol - dist
        tank += gain
        total += gain

        # If we can't reach the next pump from current start,
        # then any start between start..i also fails.
        if tank < 0:
            start = i + 1
            tank = 0

    # HackerRank guarantees there's a solution in test data,
    # but this is the correct safety check:
    return start if total >= 0 else -1

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    petrolpumps = []

    for _ in range(n):
        petrolpumps.append(list(map(int, input().rstrip().split())))

    result = truckTour(petrolpumps)

    fptr.write(str(result) + '\n')

    fptr.close()
