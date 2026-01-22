#!/bin/python3

import os
import sys

#
# Complete the solve function below.
#
def solve(t):
    #
    # Return the ID
    #
    n = len(t)
    diff = [0] * (n + 3)  # 1..n

    def add_range(l, r):
        # add +1 to [l, r] (1-indexed, inclusive), no wrap
        diff[l] += 1
        diff[r + 1] -= 1

    for i, ti in enumerate(t, start=1):  # i is 1-indexed student ID
        if ti <= 0:
            continue
        if ti >= n:
            # bad for all starts
            add_range(1, n)
            continue

        # bad starts are x in {i, i-1, ..., i-(ti-1)} mod n  => interval [L..i] circular
        L = (i - (ti - 1) - 1) % n + 1
        R = i

        if L <= R:
            add_range(L, R)
        else:
            add_range(L, n)
            add_range(1, R)

    best_id = 1
    cur = 0
    best_bad = float("inf")
    for x in range(1, n + 1):
        cur += diff[x]
        if cur < best_bad:
            best_bad = cur
            best_id = x

    return best_id

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t_count = int(input())

    t = list(map(int, input().rstrip().split()))

    id = solve(t)

    fptr.write(str(id) + '\n')

    fptr.close()
