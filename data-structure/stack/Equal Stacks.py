#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'equalStacks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY h1
#  2. INTEGER_ARRAY h2
#  3. INTEGER_ARRAY h3
#

def equalStacks(h1, h2, h3):
    # Write your code here
    s1, s2, s3 = sum(h1), sum(h2), sum(h3)
    i1 = i2 = i3 = 0  # pointers to current "top" index (since input is top->bottom)

    while True:
        # if any stack is empty, max equal height is 0
        if i1 == len(h1) or i2 == len(h2) or i3 == len(h3):
            return 0

        # all equal
        if s1 == s2 == s3:
            return s1

        # remove from the tallest stack
        if s1 >= s2 and s1 >= s3:
            s1 -= h1[i1]
            i1 += 1
        elif s2 >= s1 and s2 >= s3:
            s2 -= h2[i2]
            i2 += 1
        else:
            s3 -= h3[i3]
            i3 += 1

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n1 = int(first_multiple_input[0])

    n2 = int(first_multiple_input[1])

    n3 = int(first_multiple_input[2])

    h1 = list(map(int, input().rstrip().split()))

    h2 = list(map(int, input().rstrip().split()))

    h3 = list(map(int, input().rstrip().split()))

    result = equalStacks(h1, h2, h3)

    fptr.write(str(result) + '\n')

    fptr.close()
