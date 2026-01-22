#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'poisonousPlants' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY p as parameter.
#

def poisonousPlants(p):
    # Write your code here
    stack = []  # (pesticide, days_to_die)
    ans = 0

    for x in p:
        days = 0

        # remove left plants that are >= current (they don't help kill x)
        while stack and x <= stack[-1][0]:
            days = max(days, stack[-1][1])
            stack.pop()

        # if nothing left, x is new minimum -> never dies
        if not stack:
            days = 0
        else:
            days += 1  # will die after the max-blocking chain + 1 day

        ans = max(ans, days)
        stack.append((x, days))

    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    p = list(map(int, input().rstrip().split()))

    result = poisonousPlants(p)

    fptr.write(str(result) + '\n')

    fptr.close()
