#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'componentsInGraph' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts 2D_INTEGER_ARRAY gb as parameter.
#

def componentsInGraph(gb):
    # Write your code here
    # Node labels can go up to 2*N where N = len(gb)
    max_node = 0
    for a, b in gb:
        if a > max_node: max_node = a
        if b > max_node: max_node = b

    parent = list(range(max_node + 1))
    size = [1] * (max_node + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        # union by size
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    # Union all edges
    for a, b in gb:
        union(a, b)

    # Count component sizes (only those >= 2)
    seen = set()
    mn = 10**18
    mx = 0

    for a, b in gb:
        # only nodes that appear in edges matter
        for v in (a, b):
            r = find(v)
            if r in seen:
                continue
            seen.add(r)
            if size[r] >= 2:
                if size[r] < mn: mn = size[r]
                if size[r] > mx: mx = size[r]

    return [mn, mx]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    gb = []

    for _ in range(n):
        gb.append(list(map(int, input().rstrip().split())))

    result = componentsInGraph(gb)

    fptr.write(' '.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
