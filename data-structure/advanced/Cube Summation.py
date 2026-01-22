#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'cubeSum' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. STRING_ARRAY operations
#

def cubeSum(n, operations):
    # Write your code here
    vals = {}  # (x,y,z) -> value
    out = []

    for op in operations:
        parts = op.split()
        if parts[0] == "UPDATE":
            x, y, z, w = map(int, parts[1:])
            vals[(x, y, z)] = w
        else:  # QUERY
            x1, y1, z1, x2, y2, z2 = map(int, parts[1:])
            s = 0
            for (x, y, z), v in vals.items():
                if x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2:
                    s += v
            out.append(s)

    return out

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    T = int(input().strip())

    for T_itr in range(T):
        first_multiple_input = input().rstrip().split()

        matSize = int(first_multiple_input[0])

        m = int(first_multiple_input[1])

        ops = []

        for _ in range(m):
            ops_item = input()
            ops.append(ops_item)

        res = cubeSum(matSize, ops)

        fptr.write('\n'.join(map(str, res)))
        fptr.write('\n')

    fptr.close()
