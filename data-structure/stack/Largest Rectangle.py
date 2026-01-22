#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'largestRectangle' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts INTEGER_ARRAY h as parameter.
#

def largestRectangle(h):
    # Write your code here
    stack = []          # stores indices of increasing heights
    best = 0
    n = len(h)

    for i in range(n + 1):
        cur = 0 if i == n else h[i]   # sentinel 0 at the end to flush stack

        while stack and cur < h[stack[-1]]:
            height = h[stack.pop()]
            left_smaller_index = stack[-1] if stack else -1
            width = i - left_smaller_index - 1
            best = max(best, height * width)

        stack.append(i)

    return best

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    h = list(map(int, input().rstrip().split()))

    result = largestRectangle(h)

    fptr.write(str(result) + '\n')

    fptr.close()
