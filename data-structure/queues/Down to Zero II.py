#!/bin/python3

import math
import os
import random
import re
import sys
from collections import deque

#
# Complete the 'downToZero' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER n as parameter.
#
MAXN = 10**6
DIST = None

def precompute():
    dist = [-1] * (MAXN + 1)
    dist[0] = 0
    q = deque([0])

    while q:
        x = q.popleft()
        nd = dist[x] + 1

        # Reverse of "decrease by 1": x -> x + 1
        y = x + 1
        if y <= MAXN and dist[y] == -1:
            dist[y] = nd
            q.append(y)

        # Reverse of factor operation:
        # if forward: N=a*b -> max(a,b)
        # then reverse from x=max(a,b): x -> x*k (2 <= k <= x)
        if x >= 2:
            lim = min(x, MAXN // x)
            for k in range(2, lim + 1):
                y = x * k
                if dist[y] == -1:
                    dist[y] = nd
                    q.append(y)

    return dist

def downToZero(n):
    # Write your code here
    global DIST
    if DIST is None:
        DIST = precompute()
    return DIST[n]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        n = int(input().strip())

        result = downToZero(n)

        fptr.write(str(result) + '\n')

    fptr.close()
