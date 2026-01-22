#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY tree
#  2. 2D_INTEGER_ARRAY queries
#

def solve(tree, queries):
    # Write your code here
    from bisect import bisect_right

    class DSU:
        __slots__ = ("p", "sz")
        def __init__(self, n):
            self.p = list(range(n + 1))
            self.sz = [1] * (n + 1)

        def find(self, x):
            p = self.p
            while p[x] != x:
                p[x] = p[p[x]]
                x = p[x]
            return x

        def union_gain(self, a, b):
            ra = self.find(a)
            rb = self.find(b)
            if ra == rb:
                return 0
            if self.sz[ra] < self.sz[rb]:
                ra, rb = rb, ra
            gain = self.sz[ra] * self.sz[rb]
            self.p[rb] = ra
            self.sz[ra] += self.sz[rb]
            return gain

    # Find n from edges count
    n = len(tree) + 1

    edges = [(u, v, w) for u, v, w in tree]
    edges.sort(key=lambda x: x[2])

    dsu = DSU(n)

    uniq_w = []
    prefixF = []
    curF = 0

    i = 0
    m = len(edges)
    while i < m:
        w = edges[i][2]
        while i < m and edges[i][2] == w:
            u, v, _ = edges[i]
            curF += dsu.union_gain(u, v)
            i += 1
        uniq_w.append(w)
        prefixF.append(curF)

    def F(t):
        idx = bisect_right(uniq_w, t) - 1
        return 0 if idx < 0 else prefixF[idx]

    ans = []
    for L, R in queries:
        ans.append(F(R) - F(L - 1))

    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    tree = []

    for _ in range(n - 1):
        tree.append(list(map(int, input().rstrip().split())))

    queries = []

    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = solve(tree, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
