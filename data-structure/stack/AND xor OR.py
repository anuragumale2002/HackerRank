#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'andXorOr' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY a as parameter.
#

def andXorOr(a):
    # Write your code here
    stack = []
    ans = 0

    for x in a:
        while stack:
            ans = max(ans, stack[-1] ^ x)

            # if top is smaller, keep it (don't pop anymore)
            if stack[-1] < x:
                break

            stack.pop()

        stack.append(x)

    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    a_count = int(input().strip())

    a = list(map(int, input().rstrip().split()))

    result = andXorOr(a)

    fptr.write(str(result) + '\n')

    fptr.close()
