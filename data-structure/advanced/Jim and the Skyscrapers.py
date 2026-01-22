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
# The function accepts INTEGER_ARRAY arr as parameter.
#

def solve(arr):
    # Write your code here
    ans = 0
    stack = []  # (height, count)

    for h in arr:
        # Any smaller height groups end here (blocked by h), finalize their pairs
        while stack and stack[-1][0] < h:
            _, cnt = stack.pop()
            ans += cnt * (cnt - 1)

        if stack and stack[-1][0] == h:
            stack[-1] = (h, stack[-1][1] + 1)
        else:
            stack.append((h, 1))

    # Finalize all remaining groups
    while stack:
        _, cnt = stack.pop()
        ans += cnt * (cnt - 1)

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr_count = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    result = solve(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
