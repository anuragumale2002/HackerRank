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
#  1. INTEGER_ARRAY a
#  2. INTEGER_ARRAY w
#
class BITMax:
    # Fenwick tree for prefix maximum
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def update(self, i, val):
        while i <= self.n:
            if val > self.bit[i]:
                self.bit[i] = val
            i += i & -i

    def query(self, i):
        res = 0
        while i > 0:
            if self.bit[i] > res:
                res = self.bit[i]
            i -= i & -i
        return res

def solve(a, w):
    # Write your code here
    n = len(a)
    if n == 0:
        return 0

    # Coordinate compression of a-values
    vals = sorted(set(a))
    comp = {v: i + 1 for i, v in enumerate(vals)}  # 1-based index

    bit = BITMax(len(vals))
    best = 0

    for ai, wi in zip(a, w):
        idx = comp[ai]

        # strictly increasing => only values < ai
        prev_best = bit.query(idx - 1)
        dp = prev_best + wi

        bit.update(idx, dp)
        if dp > best:
            best = dp

    return best

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())

    for t_itr in range(t):
        n = int(input().strip())

        a = list(map(int, input().rstrip().split()))

        w = list(map(int, input().rstrip().split()))

        result = solve(a, w)

        fptr.write(str(result) + '\n')

    fptr.close()
