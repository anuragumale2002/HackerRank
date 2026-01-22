#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'twoStacks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER maxSum
#  2. INTEGER_ARRAY a
#  3. INTEGER_ARRAY b
#

def twoStacks(maxSum, a, b):
    # Write your code here
    # take as many as possible from a
    s = 0
    i = 0
    while i < len(a) and s + a[i] <= maxSum:
        s += a[i]
        i += 1

    best = i  # if we take i from a and 0 from b

    j = 0
    while j < len(b):
        s += b[j]
        j += 1

        # if sum too big, remove from a (move i back)
        while s > maxSum and i > 0:
            i -= 1
            s -= a[i]

        # if still too big, can't take more from b
        if s > maxSum:
            break

        best = max(best, i + j)

    return best

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    g = int(input().strip())

    for g_itr in range(g):
        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        maxSum = int(first_multiple_input[2])

        a = list(map(int, input().rstrip().split()))

        b = list(map(int, input().rstrip().split()))

        result = twoStacks(maxSum, a, b)

        fptr.write(str(result) + '\n')

    fptr.close()
